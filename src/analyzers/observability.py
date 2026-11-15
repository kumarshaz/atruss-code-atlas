from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from typing import Any

from src.analyzers.coverage_parser import analyze_coverage_report

_OTEL_ATTR_KEYS = frozenset({
    "code.function",
    "code.namespace",
    "code.filepath",
    "http.route",
    "url.path",
})


def _extract_attr_value(raw_val: Any) -> str:
    if isinstance(raw_val, dict):
        for key in ("stringValue", "intValue", "doubleValue", "boolValue"):
            if key in raw_val and raw_val[key] is not None:
                return str(raw_val[key])
        return ""
    if raw_val is None:
        return ""
    return str(raw_val)


def _extract_span_attributes(span: dict[str, Any]) -> dict[str, str]:
    attrs: dict[str, str] = {}
    raw_attrs = span.get("attributes")
    if isinstance(raw_attrs, dict):
        for k, v in raw_attrs.items():
            val = _extract_attr_value(v).strip()
            if val:
                attrs[str(k)] = val
    elif isinstance(raw_attrs, list):
        for entry in raw_attrs:
            if not isinstance(entry, dict):
                continue
            key = str(entry.get("key", "")).strip()
            val = _extract_attr_value(entry.get("value")).strip()
            if key and val:
                attrs[key] = val
    return attrs


def _collect_spans_from_payload(payload: Any) -> list[dict[str, Any]]:
    spans: list[dict[str, Any]] = []
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return spans

    if isinstance(payload.get("spans"), list):
        spans.extend(item for item in payload["spans"] if isinstance(item, dict))

    resource_spans = payload.get("resourceSpans")
    if isinstance(resource_spans, list):
        for res in resource_spans:
            if not isinstance(res, dict):
                continue
            scope_lists = (
                res.get("scopeSpans")
                or res.get("instrumentationLibrarySpans")
                or []
            )
            if not isinstance(scope_lists, list):
                continue
            for scope in scope_lists:
                if not isinstance(scope, dict):
                    continue
                for sp in scope.get("spans", []) if isinstance(scope.get("spans"), list) else []:
                    if isinstance(sp, dict):
                        spans.append(sp)
    return spans


def parse_otel_traces(otel_path: Path) -> dict[str, int]:
    """
    Parse OTLP JSON traces (`resourceSpans[].scopeSpans[].spans[]` or flat span lists)
    into a deterministic sorted dictionary mapping span names and attribute identifiers
    to observation counts.
    """
    if not otel_path.exists() or not otel_path.is_file():
        return {}
    try:
        payload = json.loads(otel_path.read_text(encoding="utf-8", errors="replace"))
    except (json.JSONDecodeError, OSError):
        return {}

    counts: Counter[str] = Counter()
    for span in _collect_spans_from_payload(payload):
        seen_in_span: set[str] = set()
        name = str(span.get("name", "")).strip()
        if name:
            seen_in_span.add(name)

        attrs = _extract_span_attributes(span)
        for key in _OTEL_ATTR_KEYS:
            val = attrs.get(key, "").strip()
            if val:
                seen_in_span.add(val)

        for token in seen_in_span:
            counts[token] += 1

    return dict(sorted(counts.items()))


def _norm_path(raw: str) -> str:
    cleaned = str(raw or "").strip().replace("\\", "/")
    while cleaned.startswith("./"):
        cleaned = cleaned[2:]
    return cleaned


def _parse_coverage_details(coverage_path: Path) -> dict[str, Any]:
    if not coverage_path.exists() or not coverage_path.is_file():
        return {
            "runner": "unknown",
            "coverage_percent": 0.0,
            "covered_files": set(),
            "has_files": False,
        }

    raw_text = coverage_path.read_text(encoding="utf-8", errors="replace")
    stripped = raw_text.lstrip()

    # 1. Jest / Istanbul coverage-summary.json
    if coverage_path.suffix.lower() == ".json" or stripped.startswith("{"):
        try:
            data = json.loads(raw_text)
        except json.JSONDecodeError:
            data = None
        if isinstance(data, dict) and isinstance(data.get("total"), dict):
            total = data["total"]
            pct_val = 0.0
            for metric_key in ("statements", "lines", "branches", "functions"):
                sec = total.get(metric_key)
                if isinstance(sec, dict) and sec.get("pct") is not None:
                    pct_val = float(sec["pct"])
                    break
            covered_files: set[str] = set()
            has_files = False
            for fkey, fstats in data.items():
                if fkey == "total" or not isinstance(fstats, dict):
                    continue
                has_files = True
                stmt_pct = (
                    fstats.get("statements", {}).get("pct")
                    if isinstance(fstats.get("statements"), dict)
                    else None
                )
                line_pct = (
                    fstats.get("lines", {}).get("pct")
                    if isinstance(fstats.get("lines"), dict)
                    else None
                )
                effective_pct = float(
                    stmt_pct
                    if stmt_pct is not None
                    else (line_pct if line_pct is not None else 0.0)
                )
                if effective_pct > 0.0:
                    covered_files.add(_norm_path(fkey))
            return {
                "runner": "jest",
                "coverage_percent": round(pct_val, 2),
                "covered_files": covered_files,
                "has_files": has_files,
            }

    # 2. LCOV (.info)
    if "SF:" in raw_text and (
        "LF:" in raw_text or "LH:" in raw_text or "end_of_record" in raw_text
    ):
        covered_files = set()
        has_files = False
        total_lf = 0
        total_lh = 0
        cur_file: str | None = None
        cur_lh = 0
        cur_lf = 0
        for line in raw_text.splitlines():
            if line.startswith("SF:"):
                cur_file = _norm_path(line[3:])
                cur_lh = 0
                cur_lf = 0
                has_files = True
            elif line.startswith("LF:"):
                try:
                    cur_lf = int(line[3:].strip())
                except ValueError:
                    cur_lf = 0
            elif line.startswith("LH:"):
                try:
                    cur_lh = int(line[3:].strip())
                except ValueError:
                    cur_lh = 0
            elif line.startswith("end_of_record"):
                total_lf += cur_lf
                total_lh += cur_lh
                if cur_file and cur_lh > 0:
                    covered_files.add(cur_file)
                cur_file = None
        if cur_file is not None:
            total_lf += cur_lf
            total_lh += cur_lh
            if cur_lh > 0:
                covered_files.add(cur_file)
        pct_val = round((total_lh / total_lf) * 100.0, 2) if total_lf > 0 else 0.0
        return {
            "runner": "lcov",
            "coverage_percent": pct_val,
            "covered_files": covered_files,
            "has_files": has_files,
        }

    # 3. Cobertura XML
    if "<coverage" in raw_text and "line-rate" in raw_text:
        try:
            root = ET.fromstring(raw_text)
        except ET.ParseError:
            root = None
        if root is not None and root.tag.endswith("coverage"):
            rate_str = root.attrib.get("line-rate", "0")
            try:
                pct_val = round(float(rate_str) * 100.0, 2)
            except ValueError:
                pct_val = 0.0
            covered_files = set()
            has_files = False
            for cls_el in root.iter():
                if not cls_el.tag.endswith("class"):
                    continue
                fname = cls_el.attrib.get("filename", "")
                if not fname:
                    continue
                has_files = True
                try:
                    cls_rate = float(cls_el.attrib.get("line-rate", "0"))
                except ValueError:
                    cls_rate = 0.0
                if cls_rate > 0.0:
                    covered_files.add(_norm_path(fname))
                else:
                    for line_el in cls_el.iter():
                        if line_el.tag.endswith("line"):
                            try:
                                if int(line_el.attrib.get("hits", "0")) > 0:
                                    covered_files.add(_norm_path(fname))
                                    break
                            except ValueError:
                                continue
            return {
                "runner": "cobertura",
                "coverage_percent": pct_val,
                "covered_files": covered_files,
                "has_files": has_files,
            }

    # 4. Delegate pytest-cov and JaCoCo to existing coverage_parser
    base_res = analyze_coverage_report(coverage_path)
    runner = str(base_res.get("runner", "unknown"))
    pct_val = float(base_res.get("coverage_percent", 0.0) or 0.0)
    covered_files = set()
    has_files = False

    if runner == "pytest-cov":
        for line in raw_text.splitlines():
            m = re.match(r"^\s*([^\s]+\.py)\s+\d+\s+\d+\s+(\d+)%", line)
            if m:
                has_files = True
                if int(m.group(2)) > 0:
                    covered_files.add(_norm_path(m.group(1)))
    elif runner == "jacoco":
        try:
            root = ET.fromstring(raw_text)
            for sf in root.iter():
                if sf.tag.endswith("sourcefile") and sf.attrib.get("name"):
                    has_files = True
                    for cnt in sf:
                        if (
                            cnt.tag.endswith("counter")
                            and cnt.attrib.get("type") in {"LINE", "INSTRUCTION"}
                            and int(cnt.attrib.get("covered", "0")) > 0
                        ):
                            covered_files.add(_norm_path(sf.attrib["name"]))
                            break
        except ET.ParseError:
            pass

    return {
        "runner": runner,
        "coverage_percent": pct_val,
        "covered_files": covered_files,
        "has_files": has_files,
    }


def _match_component_spans(
    comp: dict[str, Any],
    trace_counts: dict[str, int],
) -> int:
    if not trace_counts:
        return 0
    comp_name = str(comp.get("name", "")).strip()
    comp_file = _norm_path(str(comp.get("file", "")))
    comp_name_low = comp_name.lower()

    matched_keys: list[str] = []
    for key in trace_counts:
        key_clean = key.strip()
        key_low = key_clean.lower()
        key_norm_path = _norm_path(key_clean)

        if comp_name and (
            key_clean == comp_name
            or key_low == comp_name_low
            or key_low.endswith(f".{comp_name_low}")
            or key_low.endswith(f"/{comp_name_low}")
        ):
            matched_keys.append(key)
            continue

        # Match HTTP route style names like GET_users or read_users against /users
        if comp.get("type") == "API_ROUTE" and comp_name and key_clean.startswith("/"):
            route_tok = re.sub(r"[^a-z0-9]+", "_", key_low.strip("/")).strip("_")
            if route_tok and (
                comp_name_low == route_tok
                or comp_name_low.endswith(f"_{route_tok}")
                or route_tok in comp_name_low
            ):
                matched_keys.append(key)
                continue

        if (
            comp_file
            and ("/" in key_norm_path or "." in key_norm_path)
            and (
                key_norm_path == comp_file
                or comp_file.endswith(f"/{key_norm_path}")
                or key_norm_path.endswith(f"/{comp_file}")
            )
        ):
            matched_keys.append(key)

    if not matched_keys:
        return 0
    # Use the highest-count matching trace attribute/name so a single span matching both
    # code.function and code.filepath isn't double-counted.
    return max(trace_counts[k] for k in matched_keys)


def _is_file_covered(
    comp_file: str,
    covered_files: set[str],
    has_file_breakdown: bool,
    coverage_percent: float | None,
) -> bool:
    if coverage_percent is None:
        return False
    if not has_file_breakdown:
        return coverage_percent > 0.0
    norm = _norm_path(comp_file)
    if not norm:
        return False
    for cov_f in covered_files:
        if cov_f == norm or cov_f.endswith(f"/{norm}") or norm.endswith(f"/{cov_f}"):
            return True
    return False


def apply_observability_overlay(
    components: list[dict[str, Any]],
    otel_traces_path: Path | str | None = None,
    coverage_path: Path | str | None = None,
) -> dict[str, Any]:
    """
    Correlate OpenTelemetry spans and test coverage reports onto extracted architecture
    components, classifying each as HOT_PATH, COVERED_STATIC, or DEAD_UNOBSERVED.
    """
    if otel_traces_path is None and coverage_path is None:
        return {
            "enabled": False,
            "hot_paths": 0,
            "covered_static": 0,
            "dead_unobserved": 0,
        }

    trace_counts: dict[str, int] = {}
    if otel_traces_path is not None:
        trace_counts = parse_otel_traces(Path(otel_traces_path))

    cov_percent: float | None = None
    runner: str | None = None
    covered_files: set[str] = set()
    has_file_breakdown = False
    if coverage_path is not None:
        cov_info = _parse_coverage_details(Path(coverage_path))
        cov_percent = float(cov_info["coverage_percent"])
        runner = str(cov_info["runner"])
        covered_files = set(cov_info["covered_files"])
        has_file_breakdown = bool(cov_info["has_files"])

    hot_paths = 0
    covered_static = 0
    dead_unobserved = 0
    component_statuses: dict[str, str] = {}

    for comp in components:
        span_count = _match_component_spans(comp, trace_counts)
        is_covered = _is_file_covered(
            str(comp.get("file", "")),
            covered_files,
            has_file_breakdown,
            cov_percent,
        )
        if span_count > 0:
            status = "HOT_PATH"
            hot_paths += 1
        elif is_covered:
            status = "COVERED_STATIC"
            covered_static += 1
        else:
            status = "DEAD_UNOBSERVED"
            dead_unobserved += 1

        comp["observability_status"] = status
        comp["span_count"] = span_count
        comp_name = str(comp.get("name", ""))
        if comp_name:
            component_statuses[comp_name] = status

    return {
        "enabled": True,
        "coverage_percent": cov_percent,
        "runner": runner,
        "hot_paths": hot_paths,
        "covered_static": covered_static,
        "dead_unobserved": dead_unobserved,
        "observed_spans": sum(trace_counts.values()),
        "component_statuses": dict(sorted(component_statuses.items())),
    }
