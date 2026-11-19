export const SVG_NS = 'http://www.w3.org/2000/svg';
export const COPYRIGHT_WATERMARK_TEXT = `© ${new Date().getFullYear()} Shashi Kumar · kumarshaz.github.io`;

export interface DiagramThemeTokens {
    isDark: boolean;
    surfaceBg: string;
    textMuted: string;
    borderStrong: string;
    accentPrimary: string;
    fontMono: string;
}

export interface WatermarkOptions {
    includeBackground?: boolean;
    watermarkText?: string;
    tokens?: Partial<DiagramThemeTokens>;
}

/** Read active Light/Dark M3 design tokens for SVG watermark and export background parity. */
export function readDiagramThemeTokens(doc?: Document | null): DiagramThemeTokens {
    const targetDoc = doc ?? (typeof document !== 'undefined' ? document : null);
    const rootEl = targetDoc?.documentElement ?? null;
    const isDark = rootEl ? rootEl.getAttribute('data-theme') !== 'light' : true;
    const rootStyle =
        rootEl && typeof getComputedStyle === 'function' ? getComputedStyle(rootEl) : null;
    const readToken = (name: string) => rootStyle?.getPropertyValue(name).trim() || '';

    return {
        isDark,
        surfaceBg:
            readToken('--md-sys-color-surface-container-lowest') ||
            (isDark ? '#0a0e14' : '#ffffff'),
        textMuted:
            readToken('--md-sys-color-on-surface-variant') ||
            (isDark ? '#c3c6cf' : '#43474e'),
        borderStrong:
            readToken('--md-sys-color-on-surface') ||
            (isDark ? '#dfe3eb' : '#181c22'),
        accentPrimary:
            readToken('--md-sys-color-primary') ||
            (isDark ? '#a3c9ff' : '#0b57d0'),
        fontMono:
            readToken('--md-ref-typeface-mono') ||
            "'Roboto Mono', 'JetBrains Mono', ui-monospace, SFMono-Regular, monospace",
    };
}

/** Determine intrinsic SVG width and height from `viewBox` or rendered bounding box. */
export function getSvgDimensions(svgEl: SVGSVGElement): { width: number; height: number } {
    let width = 1200;
    let height = 800;
    const vbAttr = (svgEl.getAttribute('viewBox') || '').trim();
    const vbParts = vbAttr.split(/[\s,]+/).map(Number);
    if (
        vbParts.length === 4 &&
        Number.isFinite(vbParts[2]) &&
        vbParts[2] > 0 &&
        Number.isFinite(vbParts[3]) &&
        vbParts[3] > 0
    ) {
        width = Math.ceil(vbParts[2]);
        height = Math.ceil(vbParts[3]);
    } else if (typeof svgEl.getBoundingClientRect === 'function') {
        const rect = svgEl.getBoundingClientRect();
        if (rect.width > 16 && rect.height > 16) {
            width = Math.ceil(rect.width);
            height = Math.ceil(rect.height);
        }
    }
    return { width, height };
}

/** Parse the base `viewBox` tuple (`[x, y, width, height]`), preserving `data-base-viewbox` for idempotency. */
export function parseViewBox(svgEl: SVGSVGElement): [number, number, number, number] {
    const rawVb = (
        svgEl.getAttribute('data-base-viewbox') ||
        svgEl.getAttribute('viewBox') ||
        ''
    ).trim();
    const parts = rawVb.split(/[\s,]+/).map(Number);
    if (
        parts.length === 4 &&
        parts.every((n) => Number.isFinite(n)) &&
        parts[2] > 0 &&
        parts[3] > 0
    ) {
        return [parts[0], parts[1], parts[2], parts[3]];
    }
    const dims = getSvgDimensions(svgEl);
    return [0, 0, dims.width, dims.height];
}

/**
 * Inject a theme-synchronized copyright watermark footer band directly into a Mermaid `<svg>`.
 *
 * - Idempotent: caches original dimensions in `data-base-viewbox` and strips prior watermark nodes.
 * - Live renders pass `includeBackground: false` to stay transparent over the card surface.
 * - Standalone `.svg` and `.png` exports pass `includeBackground: true` so downloaded files remain
 *   self-contained and legible in both Light and Dark themes.
 */
export function applyCopyrightWatermarkToSvg(
    svgEl: SVGSVGElement,
    {
        includeBackground = false,
        watermarkText = COPYRIGHT_WATERMARK_TEXT,
        tokens,
    }: WatermarkOptions = {}
): { width: number; height: number; surfaceBg: string } {
    const doc = svgEl.ownerDocument || (typeof document !== 'undefined' ? document : null);
    if (!doc) {
        const dims = getSvgDimensions(svgEl);
        return { width: dims.width, height: dims.height, surfaceBg: '#0a0e14' };
    }

    if (!svgEl.hasAttribute('data-base-viewbox')) {
        const initialVb = (svgEl.getAttribute('viewBox') || '').trim();
        if (initialVb) {
            svgEl.setAttribute('data-base-viewbox', initialVb);
        } else {
            const dims = getSvgDimensions(svgEl);
            svgEl.setAttribute('data-base-viewbox', `0 0 ${dims.width} ${dims.height}`);
        }
    }

    svgEl
        .querySelectorAll('[data-copyright-watermark], [data-export-bg]')
        .forEach((el) => el.remove());

    const [vbX, vbY, vbW, vbH] = parseViewBox(svgEl);
    const resolvedTokens: DiagramThemeTokens = {
        ...readDiagramThemeTokens(doc),
        ...(tokens || {}),
    };
    const { surfaceBg, textMuted, borderStrong, accentPrimary, fontMono } = resolvedTokens;

    const fontSize = Number(Math.max(10.5, Math.min(20, vbW * 0.0155)).toFixed(2));
    const padX = Math.max(12, Math.round(fontSize * 1.15));
    const accentBarW = Math.max(22, Math.round(fontSize * 2.2));
    const estTextW = watermarkText.length * fontSize * 0.65;
    const minRequiredW = Math.ceil(estTextW + padX * 2 + fontSize);

    let outX = vbX;
    let outW = vbW;
    if (vbW < minRequiredW) {
        outX = Number((vbX - (minRequiredW - vbW) / 2).toFixed(2));
        outW = minRequiredW;
    }

    const topGap = Math.round(fontSize * 0.55);
    const stripH = Math.round(fontSize * 2.75);
    const outY = vbY;
    const outH = Number((vbH + stripH).toFixed(2));

    svgEl.setAttribute('viewBox', `${outX} ${outY} ${outW} ${outH}`);
    if (svgEl.hasAttribute('height') && !/%$/.test(svgEl.getAttribute('height') || '')) {
        svgEl.setAttribute('height', String(Math.ceil(outH)));
    }

    if (includeBackground) {
        const bgRect = doc.createElementNS(SVG_NS, 'rect');
        bgRect.setAttribute('data-export-bg', 'true');
        bgRect.setAttribute('x', String(outX));
        bgRect.setAttribute('y', String(outY));
        bgRect.setAttribute('width', String(outW));
        bgRect.setAttribute('height', String(outH));
        bgRect.setAttribute('fill', surfaceBg);
        bgRect.setAttribute('style', `fill: ${surfaceBg};`);
        svgEl.insertBefore(bgRect, svgEl.firstChild);
    }

    const wmGroup = doc.createElementNS(SVG_NS, 'g');
    wmGroup.setAttribute('data-copyright-watermark', 'true');
    wmGroup.setAttribute('class', 'mermaid-watermark');

    const ruleY = Number((vbY + vbH + topGap).toFixed(2));
    const strokeW = Number(Math.max(1, fontSize * 0.085).toFixed(2));

    const ruleLine = doc.createElementNS(SVG_NS, 'line');
    ruleLine.setAttribute('x1', String(Number((outX + padX).toFixed(2))));
    ruleLine.setAttribute('y1', String(ruleY));
    ruleLine.setAttribute('x2', String(Number((outX + outW - padX).toFixed(2))));
    ruleLine.setAttribute('y2', String(ruleY));
    ruleLine.setAttribute('stroke', borderStrong);
    ruleLine.setAttribute('stroke-opacity', '0.22');
    ruleLine.setAttribute('stroke-width', String(strokeW));
    ruleLine.setAttribute(
        'style',
        `stroke: ${borderStrong}; stroke-opacity: 0.22; stroke-width: ${strokeW}px;`
    );
    wmGroup.appendChild(ruleLine);

    const accentTick = doc.createElementNS(SVG_NS, 'line');
    accentTick.setAttribute('x1', String(Number((outX + padX).toFixed(2))));
    accentTick.setAttribute('y1', String(ruleY));
    accentTick.setAttribute(
        'x2',
        String(Number(Math.min(outX + outW - padX, outX + padX + accentBarW).toFixed(2)))
    );
    accentTick.setAttribute('y2', String(ruleY));
    accentTick.setAttribute('stroke', accentPrimary);
    accentTick.setAttribute('stroke-width', String(Number((strokeW * 1.8).toFixed(2))));
    accentTick.setAttribute(
        'style',
        `stroke: ${accentPrimary}; stroke-width: ${(strokeW * 1.8).toFixed(2)}px;`
    );
    wmGroup.appendChild(accentTick);

    const textY = Number((ruleY + (stripH - topGap) * 0.5 + fontSize * 0.34).toFixed(2));
    const textEl = doc.createElementNS(SVG_NS, 'text');
    textEl.setAttribute('x', String(Number((outX + outW - padX).toFixed(2))));
    textEl.setAttribute('y', String(textY));
    textEl.setAttribute('text-anchor', 'end');
    textEl.setAttribute('fill', textMuted);
    textEl.setAttribute('fill-opacity', '0.92');
    textEl.setAttribute('font-family', fontMono);
    textEl.setAttribute('font-size', String(fontSize));
    textEl.setAttribute('font-weight', '500');
    textEl.setAttribute('letter-spacing', '0.03em');
    textEl.setAttribute(
        'style',
        `fill: ${textMuted}; fill-opacity: 0.92; font-family: ${fontMono}; font-size: ${fontSize}px; font-weight: 500; letter-spacing: 0.03em;`
    );
    textEl.textContent = watermarkText;
    wmGroup.appendChild(textEl);

    svgEl.appendChild(wmGroup);
    return { width: Math.ceil(outW), height: Math.ceil(outH), surfaceBg };
}

/** Split optional Mermaid YAML frontmatter (`--- ... ---`) from the diagram body. */
export function stripDiagramFrontmatter(src: string): { frontmatter: string; body: string } {
    const trimmed = String(src || '').trim();
    const fmMatch = trimmed.match(/^---\s*\n([\s\S]*?)\n---\s*\n([\s\S]*)$/);
    if (fmMatch) {
        return { frontmatter: fmMatch[1], body: fmMatch[2].trim() };
    }
    return { frontmatter: '', body: trimmed };
}

/**
 * Resolve a plain, descriptive title for a Mermaid diagram following the BlogPost precedence order:
 * 1. Explicit `%% title: ...` comment directive
 * 2. Explicit `accTitle: ...` accessibility directive
 * 3. YAML frontmatter `title:`
 * 4. Native `title ...` statement (`timeline`, `gantt`, `pie`, `journey`, `xychart-beta`)
 * 5. Mindmap `root(...)` label
 * 6. Nearest preceding Markdown heading (`h1`–`h4`) in the surrounding content container
 * 7. Provided `fallbackTitle` or neutral `Figure N`
 */
export function resolveDiagramTitle(
    rawSource: string,
    sourceEl?: Element | null,
    index = 0,
    fallbackTitle?: string
): string {
    const source = String(rawSource || '');

    // 1. Explicit comment directive: `%% title: ...`
    const commentMatch = source.match(/^\s*%%\s*title\s*:\s*(.+)$/im);
    if (commentMatch && commentMatch[1].trim()) {
        return commentMatch[1].trim();
    }

    // 2. Explicit Mermaid accessibility title: `accTitle: ...`
    const accMatch = source.match(/^\s*accTitle\s*:\s*(.+)$/im);
    if (accMatch && accMatch[1].trim()) {
        return accMatch[1].trim();
    }

    const { frontmatter, body } = stripDiagramFrontmatter(source);

    // 3. Explicit YAML frontmatter `title:`
    if (frontmatter) {
        const fmTitleMatch = frontmatter.match(/^\s*title\s*:\s*(.+)$/im);
        if (fmTitleMatch) {
            const cleanedFmTitle = fmTitleMatch[1]
                .trim()
                .replace(/^["']|["']$/g, '')
                .trim();
            if (cleanedFmTitle) return cleanedFmTitle;
        }
    }

    // Determine non-comment diagram body header line
    const firstCodeLine =
        body
            .split('\n')
            .map((l) => l.trim())
            .find((l) => l.length > 0 && !l.startsWith('%%')) || '';

    // 4. Native `title ...` statement in timeline/gantt/pie/journey/xychart-beta
    if (/^(?:timeline|gantt|pie|journey|xychart-beta)\b/i.test(firstCodeLine)) {
        const nativeTitleMatch = body.match(/^\s*title\s+(.+)$/im);
        if (nativeTitleMatch && nativeTitleMatch[1].trim()) {
            return nativeTitleMatch[1].trim();
        }
    }

    // 5. Mindmap root node label (`root(("..."))`)
    if (/^mindmap\b/i.test(firstCodeLine)) {
        const rootLineMatch = body.match(/^\s*root\s*(.+)$/im);
        if (rootLineMatch) {
            let rootRaw = rootLineMatch[1].trim();
            for (const [open, close] of [
                ['(((', ')))'],
                ['((', '))'],
                ['([', '])'],
                ['[[', ']]'],
                ['{{', '}}'],
                ['))', '(('],
                ['(', ')'],
                ['[', ']'],
                ['{', '}'],
            ]) {
                if (
                    rootRaw.startsWith(open) &&
                    rootRaw.endsWith(close) &&
                    rootRaw.length > open.length + close.length
                ) {
                    rootRaw = rootRaw.slice(open.length, -close.length).trim();
                    break;
                }
            }
            const cleanedRoot = rootRaw
                .replace(/^["']|["']$/g, '')
                .replace(/<br\s*\/?>|\\n/gi, ' ')
                .replace(/\s+/g, ' ')
                .trim();
            if (cleanedRoot) return cleanedRoot;
        }
    }

    // 6. Nearest preceding Markdown heading within report or article prose
    if (sourceEl && typeof sourceEl.closest === 'function') {
        const proseRoot = sourceEl.closest(
            '.markdown-content, #article-prose, article, main'
        );
        const followingFlag =
            typeof Node !== 'undefined' && typeof Node.DOCUMENT_POSITION_FOLLOWING === 'number'
                ? Node.DOCUMENT_POSITION_FOLLOWING
                : 4;
        if (proseRoot) {
            const headingsBefore = Array.from(proseRoot.querySelectorAll('h1, h2, h3, h4')).filter(
                (h) => Boolean(h.compareDocumentPosition(sourceEl) & followingFlag)
            );
            const nearest = headingsBefore[headingsBefore.length - 1];
            if (nearest) {
                const headingText = (nearest.textContent || '')
                    .replace(/\s+/g, ' ')
                    .trim()
                    .replace(/^(?:section\s+\d+\s*[:.-]\s*|\d+(?:\.\d+)*\.\s+|[A-Z]\.\s+)/i, '')
                    .trim();
                if (headingText) return headingText;
            }
        }
    }

    // 7. Explicit fallback or neutral figure fallback
    if (fallbackTitle && fallbackTitle.trim()) {
        return fallbackTitle.trim();
    }
    return `Figure ${index + 1}`;
}

function normalizeSlugRaw(value: string): string {
    return String(value || '')
        .toLowerCase()
        .replace(/→/g, '-to-')
        .replace(/&/g, ' and ')
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/^-+|-+$/g, '');
}

/** Convert a descriptive title or prefix segment into a clean lowercase kebab-case filename slug. */
export function slugifySegment(value: string, maxLength = 48): string {
    return normalizeSlugRaw(value).slice(0, maxLength).replace(/-+$/g, '');
}

/**
 * Build a descriptive, collision-free SVG/PNG filename base from a context prefix and diagram title.
 * Avoids repeating the prefix when the title already starts with the same slug (e.g. `org/repo — ...`),
 * while preserving up to 48 characters of the descriptive title segment.
 */
export function buildDiagramFilename(
    prefix: string,
    title: string,
    fallbackIndex = 0,
    usedCounts?: Map<string, number>
): string {
    const cleanPrefix = normalizeSlugRaw(prefix);
    const fullTitleSlug = normalizeSlugRaw(title);

    let rawBase: string;
    if (cleanPrefix && fullTitleSlug) {
        if (fullTitleSlug === cleanPrefix) {
            rawBase = cleanPrefix;
        } else if (fullTitleSlug.startsWith(`${cleanPrefix}-`)) {
            const suffix = fullTitleSlug
                .slice(cleanPrefix.length + 1)
                .slice(0, 48)
                .replace(/-+$/g, '');
            rawBase = suffix ? `${cleanPrefix}-${suffix}` : cleanPrefix;
        } else {
            const titleSlug = fullTitleSlug.slice(0, 48).replace(/-+$/g, '');
            rawBase = titleSlug ? `${cleanPrefix}-${titleSlug}` : cleanPrefix;
        }
    } else if (fullTitleSlug) {
        rawBase = fullTitleSlug.slice(0, 48).replace(/-+$/g, '');
    } else if (cleanPrefix) {
        rawBase = `${cleanPrefix}-figure-${fallbackIndex + 1}`;
    } else {
        rawBase = `figure-${fallbackIndex + 1}`;
    }

    if (!usedCounts) return rawBase;
    const seen = (usedCounts.get(rawBase) ?? 0) + 1;
    usedCounts.set(rawBase, seen);
    return seen > 1 ? `${rawBase}-${seen}` : rawBase;
}
