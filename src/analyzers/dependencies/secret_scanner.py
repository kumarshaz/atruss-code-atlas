from __future__ import annotations

import math
import os
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from src.analyzers.dependencies.manifest_parser import SKIP_DIRS
from src.models.artifacts import SecretFinding

_LOCKFILE_NAMES = frozenset({
    "uv.lock",
    "poetry.lock",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "packages.lock.json",
    "cargo.lock",
    "gemfile.lock",
    "composer.lock",
    "go.sum",
    "pipfile.lock",
    "shrinkwrap.json",
    "npm-shrinkwrap.json",
    "bun.lockb",
    "bun.lock",
    "flake.lock",
})

_BINARY_OR_ASSET_EXTENSIONS = frozenset({
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".ico",
    ".webp",
    ".avif",
    ".tiff",
    ".pdf",
    ".zip",
    ".tar",
    ".gz",
    ".tgz",
    ".bz2",
    ".xz",
    ".7z",
    ".rar",
    ".jar",
    ".war",
    ".ear",
    ".dll",
    ".exe",
    ".so",
    ".dylib",
    ".a",
    ".lib",
    ".o",
    ".obj",
    ".pyc",
    ".pyo",
    ".pyd",
    ".class",
    ".wasm",
    ".sqlite",
    ".sqlite3",
    ".db",
    ".bin",
    ".dat",
    ".mp3",
    ".mp4",
    ".wav",
    ".avi",
    ".mov",
    ".woff",
    ".woff2",
    ".ttf",
    ".otf",
    ".eot",
    ".lock",
    ".map",
})

_PLACEHOLDER_TOKENS = (
    "example",
    "dummy",
    "placeholder",
    "changeme",
    "test_token",
)

_HIGH_CONFIDENCE_PATTERNS: tuple[tuple[str, str, str, re.Pattern[str], str], ...] = (
    (
        "ATRUSS-SEC-001",
        "AWS_ACCESS_KEY",
        "CRITICAL",
        re.compile(r"\b(AKIA[0-9A-Z]{16})\b"),
        "Potential hardcoded AWS Access Key ID detected.",
    ),
    (
        "ATRUSS-SEC-002",
        "GITHUB_TOKEN",
        "CRITICAL",
        re.compile(r"\b(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
        "Potential hardcoded GitHub Personal Access Token detected.",
    ),
    (
        "ATRUSS-SEC-003",
        "API_SECRET_KEY",
        "CRITICAL",
        re.compile(r"\b(sk-(?:proj-)?[A-Za-z0-9]{20,})\b"),
        "Potential hardcoded API secret key (`sk-...`) detected.",
    ),
)

_PRIVATE_KEY_BEGIN_RE = re.compile(
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
)
_PRIVATE_KEY_END_RE = re.compile(
    r"-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
)

_ENTROPY_QUOTED_RE = re.compile(
    r"""(?i)[A-Za-z0-9_.-]*(?:secret|token|key|password|passwd|pwd|auth)[A-Za-z0-9_.-]*"""
    r"""['"]?\s*(?:=|:|:=)\s*['"]([^'"\s]{20,})['"]"""
)
_ENTROPY_UNQUOTED_RE = re.compile(
    r"""(?i)^[ \t]*(?:export[ \t]+)?"""
    r"""[A-Za-z0-9_.-]*(?:secret|token|key|password|passwd|pwd|auth)[A-Za-z0-9_.-]*"""
    r"""\s*(?:=|:)\s*([^\s"'#;,()\[\]{}]{20,})(?:\s|$|#)"""
)
_UNQUOTED_CONFIG_NAMES = frozenset({".env", "dockerfile", ".npmrc", ".pypirc", ".netrc"})
_UNQUOTED_CONFIG_EXTENSIONS = frozenset({
    ".env",
    ".yml",
    ".yaml",
    ".properties",
    ".ini",
    ".cfg",
    ".conf",
    ".sh",
    ".bash",
    ".zsh",
    ".txt",
})

_MAX_SCAN_BYTES = 2 * 1024 * 1024
_ENTROPY_THRESHOLD = 4.5


def shannon_entropy(text: str) -> float:
    """Compute Shannon entropy (bits per character) for a candidate secret string."""
    if not text:
        return 0.0
    length = len(text)
    counts = Counter(text)
    return -sum((count / length) * math.log2(count / length) for count in counts.values())


@dataclass(frozen=True)
class _GitIgnoreRule:
    base_rel: str
    negated: bool
    dir_only: bool
    anchored: bool
    regex: re.Pattern[str]


def _glob_to_regex(pattern: str, *, anchored: bool) -> re.Pattern[str]:
    parts: list[str] = []
    i = 0
    n = len(pattern)
    while i < n:
        ch = pattern[i]
        if ch == "*":
            if i + 1 < n and pattern[i + 1] == "*":
                if i + 2 < n and pattern[i + 2] == "/":
                    parts.append("(?:.+/)?")
                    i += 3
                    continue
                parts.append(".*")
                i += 2
                continue
            parts.append("[^/]*")
            i += 1
        elif ch == "?":
            parts.append("[^/]")
            i += 1
        elif ch == "[":
            end = pattern.find("]", i + 1)
            if end != -1:
                inner = pattern[i + 1 : end]
                if inner.startswith("!"):
                    inner = "^" + inner[1:]
                parts.append(f"[{inner}]")
                i = end + 1
                continue
            parts.append(re.escape(ch))
            i += 1
        else:
            parts.append(re.escape(ch))
            i += 1

    body = "".join(parts)
    if anchored:
        return re.compile(rf"^{body}(?:/.*)?$")
    return re.compile(rf"(?:^|/){body}(?:/.*)?$")


def _parse_gitignore_file(gitignore_path: Path, base_rel: str) -> list[_GitIgnoreRule]:
    try:
        content = gitignore_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []

    rules: list[_GitIgnoreRule] = []
    for raw_line in content.splitlines():
        line = raw_line.rstrip("\r")
        if not line or line.lstrip().startswith("#"):
            continue
        line = line.rstrip() if not line.endswith("\\ ") else line[:-2] + " "
        if not line:
            continue

        negated = False
        if line.startswith("!"):
            negated = True
            line = line[1:]
        elif line.startswith("\\!") or line.startswith("\\#"):
            line = line[1:]

        if not line:
            continue

        dir_only = line.endswith("/")
        if dir_only:
            line = line.rstrip("/")
        if not line:
            continue

        anchored = "/" in line
        clean_pat = line.lstrip("/")
        if not clean_pat:
            continue

        rules.append(
            _GitIgnoreRule(
                base_rel=base_rel,
                negated=negated,
                dir_only=dir_only,
                anchored=anchored,
                regex=_glob_to_regex(clean_pat, anchored=anchored),
            )
        )
    return rules


def _is_gitignored(rel_posix: str, is_dir: bool, rules: list[_GitIgnoreRule]) -> bool:
    ignored = False
    for rule in rules:
        if rule.base_rel:
            prefix = f"{rule.base_rel}/"
            if not rel_posix.startswith(prefix):
                continue
            scoped_rel = rel_posix[len(prefix) :]
        else:
            scoped_rel = rel_posix

        if rule.dir_only and not is_dir:
            dir_prefixes: list[str] = []
            cur = ""
            for part in scoped_rel.split("/")[:-1]:
                cur = f"{cur}/{part}" if cur else part
                dir_prefixes.append(cur)
            matched = any(bool(rule.regex.match(dp)) for dp in dir_prefixes)
        else:
            matched = bool(rule.regex.match(scoped_rel))

        if matched:
            ignored = not rule.negated
    return ignored


def _is_placeholder(text: str) -> bool:
    low = text.lower()
    return any(tok in low for tok in _PLACEHOLDER_TOKENS)


def _should_skip_entropy_candidate(candidate: str) -> bool:
    low = candidate.lower()
    if low.startswith(("http://", "https://", "pkg:", "urn:", "arn:aws:", "${", "{{")):
        return True
    if any(ch in candidate for ch in ("(", ")", "[", "]", "{", "}")):
        return True
    return bool(re.match(r"^(?:/[A-Za-z0-9_.-]+){3,}$", candidate))


def _redact_secret_in_line(line: str, secret: str) -> str:
    prefix = secret[:4] if len(secret) > 8 else ""
    replacement = f"{prefix}***REDACTED***"
    redacted_line = line.strip().replace(secret, replacement)
    if len(redacted_line) > 160:
        idx = redacted_line.find(replacement)
        if idx == -1:
            return redacted_line[:157] + "..."
        start = max(0, idx - 40)
        end = min(len(redacted_line), idx + len(replacement) + 40)
        snippet = redacted_line[start:end]
        if start > 0:
            snippet = "..." + snippet
        if end < len(redacted_line):
            snippet = snippet + "..."
        return snippet
    return redacted_line


def _is_scannable_file(path: Path) -> bool:
    low_name = path.name.lower()
    if low_name in _LOCKFILE_NAMES:
        return False
    if low_name.endswith((".min.js", ".min.css", ".cdx.json")):
        return False
    if path.suffix.lower() in _BINARY_OR_ASSET_EXTENSIONS:
        return False
    try:
        if path.stat().st_size > _MAX_SCAN_BYTES:
            return False
        with path.open("rb") as fh:
            head = fh.read(8192)
        if b"\x00" in head:
            return False
    except OSError:
        return False
    return True


def _scan_file_lines(rel_path: str, text: str) -> list[SecretFinding]:
    lines = text.splitlines()
    findings: list[SecretFinding] = []
    private_key_lines: set[int] = set()

    # 1. Multi-line private key headers
    idx = 0
    while idx < len(lines):
        line_no = idx + 1
        line = lines[idx]
        if _PRIVATE_KEY_BEGIN_RE.search(line):
            end_line = line_no
            j = idx + 1
            while j < len(lines) and j - idx <= 200:
                if _PRIVATE_KEY_END_RE.search(lines[j]):
                    end_line = j + 1
                    break
                j += 1
            for ln in range(line_no, end_line + 1):
                private_key_lines.add(ln)
            findings.append(
                SecretFinding(
                    rule_id="ATRUSS-SEC-004",
                    type="PRIVATE_KEY",
                    severity="CRITICAL",
                    file_source=rel_path,
                    start_line=line_no,
                    end_line=end_line,
                    redacted_snippet="-----BEGIN ... PRIVATE KEY----- [REDACTED]",
                    entropy=round(shannon_entropy(line), 4),
                    message="Private key material header detected.",
                )
            )
            idx = end_line
            continue
        idx += 1

    # 2. Line-by-line regex + Shannon entropy scanning
    for idx, line in enumerate(lines, start=1):
        if idx in private_key_lines:
            continue

        matched_tokens_on_line: set[str] = set()

        for rule_id, sec_type, severity, pattern, message in _HIGH_CONFIDENCE_PATTERNS:
            for m in pattern.finditer(line):
                secret_val = m.group(1)
                key_ctx = line[: m.start()]
                if _is_placeholder(secret_val) or _is_placeholder(key_ctx):
                    continue
                matched_tokens_on_line.add(secret_val)
                findings.append(
                    SecretFinding(
                        rule_id=rule_id,
                        type=sec_type,
                        severity=severity,
                        file_source=rel_path,
                        start_line=idx,
                        end_line=idx,
                        redacted_snippet=_redact_secret_in_line(line, secret_val),
                        entropy=round(shannon_entropy(secret_val), 4),
                        message=message,
                    )
                )

        # High-entropy assigned/quoted secret detection
        rel_path_low = rel_path.lower()
        base_name = rel_path_low.rsplit("/", 1)[-1]
        allow_unquoted = (
            base_name in _UNQUOTED_CONFIG_NAMES
            or base_name.startswith(".env.")
            or Path(base_name).suffix in _UNQUOTED_CONFIG_EXTENSIONS
        )
        entropy_patterns = (
            (_ENTROPY_QUOTED_RE, _ENTROPY_UNQUOTED_RE)
            if allow_unquoted
            else (_ENTROPY_QUOTED_RE,)
        )
        for ent_re in entropy_patterns:
            for m in ent_re.finditer(line):
                secret_val = m.group(1)
                if secret_val in matched_tokens_on_line:
                    continue
                if _should_skip_entropy_candidate(secret_val):
                    continue
                if _is_placeholder(m.group(0)):
                    continue
                ent = shannon_entropy(secret_val)
                if ent > _ENTROPY_THRESHOLD:
                    matched_tokens_on_line.add(secret_val)
                    findings.append(
                        SecretFinding(
                            rule_id="ATRUSS-SEC-005",
                            type="HIGH_ENTROPY_SECRET",
                            severity="HIGH",
                            file_source=rel_path,
                            start_line=idx,
                            end_line=idx,
                            redacted_snippet=_redact_secret_in_line(line, secret_val),
                            entropy=round(ent, 4),
                            message=(
                                f"High-entropy credential candidate (H={ent:.2f} > 4.5) detected."
                            ),
                        )
                    )

    return findings


def scan_repository_secrets(repo_dir: Path) -> list[SecretFinding]:
    """
    Scan source and configuration files inside `repo_dir` for hardcoded secrets
    and high-entropy credentials while honoring `.gitignore`, skip directories,
    lockfiles, binaries, and placeholder patterns.
    """
    if not repo_dir.exists() or not repo_dir.is_dir():
        return []

    root_rules: list[_GitIgnoreRule] = []
    root_gitignore = repo_dir / ".gitignore"
    if root_gitignore.is_file():
        root_rules.extend(_parse_gitignore_file(root_gitignore, ""))

    rules_by_dir: dict[str, list[_GitIgnoreRule]] = {"": root_rules}
    has_negation = any(r.negated for r in root_rules)
    findings: list[SecretFinding] = []

    for root, dirnames, filenames in os.walk(repo_dir):
        root_path = Path(root)
        rel_root = root_path.relative_to(repo_dir)
        rel_root_posix = "" if rel_root == Path(".") else rel_root.as_posix()

        parent_posix = (
            ""
            if not rel_root_posix or "/" not in rel_root_posix
            else rel_root_posix.rsplit("/", 1)[0]
        )
        local_rules = list(rules_by_dir.get(parent_posix, root_rules))
        if rel_root_posix:
            nested_gi = root_path / ".gitignore"
            if nested_gi.is_file():
                local_rules.extend(_parse_gitignore_file(nested_gi, rel_root_posix))
                if any(r.negated for r in local_rules):
                    has_negation = True
        rules_by_dir[rel_root_posix] = local_rules

        kept_dirs: list[str] = []
        for d in sorted(dirnames):
            if d in SKIP_DIRS:
                continue
            d_rel = f"{rel_root_posix}/{d}" if rel_root_posix else d
            if not has_negation and _is_gitignored(d_rel, True, local_rules):
                continue
            kept_dirs.append(d)
        dirnames[:] = kept_dirs

        for fname in sorted(filenames):
            if fname == ".gitignore":
                continue
            fpath = root_path / fname
            rel_posix = f"{rel_root_posix}/{fname}" if rel_root_posix else fname
            if _is_gitignored(rel_posix, False, local_rules):
                continue
            if not _is_scannable_file(fpath):
                continue
            try:
                text = fpath.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            findings.extend(_scan_file_lines(rel_posix, text))

    return sorted(
        findings,
        key=lambda f: (f.file_source, f.start_line, f.end_line, f.rule_id, f.redacted_snippet),
    )
