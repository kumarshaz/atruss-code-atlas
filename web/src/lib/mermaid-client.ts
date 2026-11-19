import mermaid from 'mermaid';
import elkLayouts from '@mermaid-js/layout-elk';
import {
    COPYRIGHT_WATERMARK_TEXT,
    SVG_NS,
    applyCopyrightWatermarkToSvg,
    buildDiagramFilename,
    getSvgDimensions,
    parseViewBox,
    readDiagramThemeTokens,
    resolveDiagramTitle,
    slugifySegment,
    stripDiagramFrontmatter,
    type DiagramThemeTokens,
    type WatermarkOptions,
} from './diagram-metadata';

export {
    COPYRIGHT_WATERMARK_TEXT,
    SVG_NS,
    applyCopyrightWatermarkToSvg,
    buildDiagramFilename,
    getSvgDimensions,
    parseViewBox,
    readDiagramThemeTokens,
    resolveDiagramTitle,
    slugifySegment,
    stripDiagramFrontmatter,
    type DiagramThemeTokens,
    type WatermarkOptions,
};

let elkRegistered = false;
function ensureLayoutLoaders(): void {
    if (!elkRegistered && typeof mermaid.registerLayoutLoaders === 'function') {
        mermaid.registerLayoutLoaders(elkLayouts);
        elkRegistered = true;
    }
}

/** Normalize an arbitrary string into a safe Mermaid node identifier. */
export function safeId(raw: string): string {
    const cleaned = String(raw || 'n').replace(/[^a-zA-Z0-9_]/g, '_');
    return /^[0-9]/.test(cleaned) ? `n_${cleaned}` : cleaned || 'n';
}

/** Sanitize a string for safe embedding inside Mermaid quoted labels. */
export function safeLabel(raw: string): string {
    return String(raw || '')
        .replace(/"/g, "'")
        .replace(/[\r\n]+/g, ' ')
        .replace(/\[/g, '(')
        .replace(/\]/g, ')')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
}

/** Return semantic Mermaid `classDef` lines aligned with the active light/dark theme. */
export function getMermaidClassDefs(isDark?: boolean): string[] {
    const dark =
        typeof isDark === 'boolean'
            ? isDark
            : typeof document !== 'undefined' &&
              document.documentElement.getAttribute('data-theme') !== 'light';

    if (dark) {
        return [
            '  classDef atlasRoot fill:#004882,stroke:#a3c9ff,stroke-width:2px,color:#d3e4ff,font-weight:600',
            '  classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb,font-weight:600',
            '  classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb',
            '  classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb',
            '  classDef atlasStage fill:#3c4858,stroke:#bbc7db,stroke-width:1px,color:#d7e3f7',
            '  classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6',
            '  classDef atlasAlert fill:#93000a,stroke:#ffb4ab,stroke-width:1.5px,color:#ffdad6',
            '  classDef atlasMore fill:#252a31,stroke:#8d9199,stroke-dasharray:4 4,color:#c3c6cf',
        ];
    }

    return [
        '  classDef atlasRoot fill:#d3e4ff,stroke:#004882,stroke-width:2px,color:#001d36,font-weight:600',
        '  classDef atlasCategory fill:#FAF9F5,stroke:#C84B20,stroke-width:1.5px,color:#111111,font-weight:600',
        '  classDef atlasWorkflow fill:#FAF9F5,stroke:#4338ca,stroke-width:1.5px,color:#181c22',
        '  classDef atlasJob fill:#f1f5f9,stroke:#64748b,stroke-width:1px,color:#181c22',
        '  classDef atlasStage fill:#e2e8f0,stroke:#475569,stroke-width:1px,color:#1e293b',
        '  classDef atlasTarget fill:#dcfce7,stroke:#15803d,stroke-width:1.5px,color:#14532d',
        '  classDef atlasAlert fill:#fee2e2,stroke:#b91c1c,stroke-width:1.5px,color:#7f1d1d',
        '  classDef atlasMore fill:#E7E5DD,stroke:#64748b,stroke-dasharray:4 4,color:#334155',
    ];
}

/** Configure Mermaid with theme-aware dark/light blueprint/M3 styling and safe size caps. */
export function configureMermaid(htmlLabels = true): void {
    ensureLayoutLoaders();
    const isDark = document.documentElement.getAttribute('data-theme') !== 'light';
    mermaid.initialize({
        startOnLoad: false,
        layout: 'elk',
        theme: 'base',
        themeVariables: isDark
            ? {
                  fontFamily:
                      "'Roboto Mono', 'JetBrains Mono', ui-monospace, SFMono-Regular, monospace",
                  fontSize: '13px',
                  background: '#0f141a',
                  primaryColor: '#212428',
                  primaryTextColor: '#dfe3eb',
                  primaryBorderColor: '#E87A48',
                  lineColor: '#9A968E',
                  secondaryColor: '#1b2026',
                  secondaryTextColor: '#dfe3eb',
                  secondaryBorderColor: '#43474e',
                  tertiaryColor: '#191B1E',
                  tertiaryTextColor: '#c3c6cf',
                  tertiaryBorderColor: '#43474e',
                  clusterBkg: '#191B1E',
                  clusterBorder: '#43474e',
                  edgeLabelBackground: '#171c22',
                  nodeTextColor: '#dfe3eb',
              }
            : {
                  fontFamily:
                      "'Roboto Mono', 'JetBrains Mono', ui-monospace, SFMono-Regular, monospace",
                  fontSize: '13px',
                  background: '#f8f9ff',
                  primaryColor: '#FAF9F5',
                  primaryTextColor: '#111111',
                  primaryBorderColor: '#C84B20',
                  lineColor: '#262523',
                  secondaryColor: '#E7E5DD',
                  secondaryTextColor: '#181c22',
                  secondaryBorderColor: '#94a3b8',
                  tertiaryColor: '#f1f5f9',
                  tertiaryTextColor: '#181c22',
                  tertiaryBorderColor: '#cbd5e1',
                  clusterBkg: '#f1f5f9',
                  clusterBorder: '#94a3b8',
                  edgeLabelBackground: '#FAF9F5',
                  nodeTextColor: '#111111',
              },
        maxTextSize: 200000,
        flowchart: {
            useMaxWidth: true,
            htmlLabels,
            nodeSpacing: 28,
            rankSpacing: 44,
            curve: 'basis',
        },
    });
}

/**
 * Replace any statically baked `classDef atlas*` lines with the active light/dark theme palette
 * so static Arc42 Markdown diagrams remain high-contrast in both light and dark modes.
 */
export function adaptMermaidSourceToTheme(source: string): string {
    if (!source || !source.includes('classDef atlas')) return source;
    const rawLines = source.split(/\r?\n/);
    const filtered = rawLines.filter((line) => !/^\s*classDef\s+atlas[A-Za-z0-9_]+\b/.test(line));
    const headerIdx = filtered.findIndex((line) =>
        /^\s*(?:graph|flowchart)\s+(?:TD|TB|LR|RL|BT)\b/i.test(line)
    );
    const activeDefs = getMermaidClassDefs();
    if (headerIdx >= 0) {
        filtered.splice(headerIdx + 1, 0, ...activeDefs);
        return filtered.join('\n');
    }
    return [...activeDefs, ...filtered].join('\n');
}

/** Render a Mermaid definition string into SVG markup using the active theme. */
export async function renderMermaidSvg(
    prefix: string,
    graphDef: string,
    htmlLabels = true
): Promise<string> {
    configureMermaid(htmlLabels);
    const themedDef = adaptMermaidSourceToTheme(graphDef);
    const renderId = `${safeId(prefix)}-${Math.random().toString(36).slice(2, 10)}`;
    const { svg } = await mermaid.render(renderId, themedDef);
    if (!htmlLabels) configureMermaid(true);
    return svg;
}

/** Style an injected Mermaid SVG for responsive full-width layout inside cards. */
export function applyResponsiveSvgStyle(svgEl: SVGSVGElement | null): void {
    if (!svgEl) return;
    const { width: vbW } = getSvgDimensions(svgEl);
    svgEl.style.maxWidth = vbW ? `min(100%, ${vbW}px)` : '100%';
    svgEl.style.width = '100%';
    svgEl.style.height = 'auto';
    svgEl.style.display = 'block';
    svgEl.style.margin = '0 auto';
}

/**
 * Apply the live theme-synchronized copyright watermark and responsive layout styling
 * to a newly injected Mermaid `<svg>` element, then synchronize enclosing zoom state.
 */
export function finalizeRenderedMermaidSvg(svgEl: SVGSVGElement | null): void {
    if (!svgEl) return;
    applyCopyrightWatermarkToSvg(svgEl, { includeBackground: false });
    applyResponsiveSvgStyle(svgEl);
    const zoomBox = svgEl.closest<HTMLElement>('[data-zoom-container="true"]');
    if (zoomBox) {
        zoomBox.dispatchEvent(new CustomEvent('atruss:sync-zoom'));
    }
}

/** Update a diagram card's visible title, accessible labels, and SVG/PNG download button tooltips. */
export function syncDiagramCardTitle(cardEl: HTMLElement | null, diagramTitle: string): void {
    if (!cardEl || !diagramTitle) return;
    const cleanTitle = diagramTitle.trim();
    if (!cleanTitle) return;

    cardEl.dataset.diagramTitle = cleanTitle;
    cardEl.setAttribute('aria-label', cleanTitle);

    const ownsEl = (el: Element) => {
        const nearest = el.closest('[data-zoom-container="true"]');
        return !nearest || nearest === cardEl;
    };

    const titleEl = Array.from(cardEl.querySelectorAll<HTMLElement>('[data-diagram-title]')).find(
        ownsEl
    );
    if (titleEl) {
        titleEl.textContent = cleanTitle;
    }

    const toolbar = Array.from(
        cardEl.querySelectorAll<HTMLElement>('[role="toolbar"], [role="group"]')
    ).find(ownsEl);
    if (toolbar) {
        toolbar.setAttribute('aria-label', `Controls for ${cleanTitle}`);
    }

    Array.from(cardEl.querySelectorAll<HTMLButtonElement>('[data-export-format]'))
        .filter(ownsEl)
        .forEach((btn) => {
            const fmt = (btn.dataset.exportFormat || 'svg').toLowerCase();
            const label =
                fmt === 'png'
                    ? `Download high-resolution PNG: ${cleanTitle}`
                    : `Download SVG: ${cleanTitle}`;
            btn.title = label;
            btn.setAttribute('aria-label', label);
        });
}

/** Check whether an existing Mermaid SVG failed layout, lacks watermark, or used a different theme. */
export function needsVisibleMermaidRepair(hostEl: HTMLElement): boolean {
    const activeTheme =
        typeof document !== 'undefined' &&
        document.documentElement.getAttribute('data-theme') === 'light'
            ? 'light'
            : 'dark';
    const svgEl = hostEl.querySelector<SVGSVGElement>('svg');
    if (!svgEl) return true;
    if (!svgEl.querySelector('[data-copyright-watermark]')) return true;
    if (hostEl.dataset.archRenderedVisible === 'true' && hostEl.dataset.archTheme === activeTheme) {
        return false;
    }
    if (hostEl.dataset.archTheme !== activeTheme) return true;
    const vb = (svgEl.getAttribute('viewBox') || '').trim();
    if (vb === '-8 -8 16 16') return true;
    const rect = svgEl.getBoundingClientRect();
    return rect.width <= 24 || rect.height <= 24;
}

/** Snapshot raw Mermaid source into `data-diagram` before any renderer replaces it with SVG. */
export function snapshotMermaidSources(scope: ParentNode = document): void {
    scope.querySelectorAll<HTMLElement>('pre.mermaid, .m3-mermaid-host').forEach((el) => {
        if (el.hasAttribute('data-diagram')) return;
        if (el.querySelector('svg')) return;
        const raw = (el.textContent || '').trim();
        if (raw && !raw.startsWith('#mermaid-') && !raw.includes('@keyframes')) {
            el.setAttribute('data-diagram', raw);
        }
    });
}

function makeBlueprintToolbarBtn(
    text: string,
    title: string,
    extraClass?: string
): HTMLButtonElement {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = extraClass ? `mermaid-toolbar-btn ${extraClass}` : 'mermaid-toolbar-btn';
    btn.textContent = text;
    btn.title = title;
    btn.setAttribute('aria-label', title);
    return btn;
}

function makeBlueprintSep(): HTMLSpanElement {
    const sep = document.createElement('span');
    sep.className = 'mermaid-toolbar-sep';
    sep.setAttribute('aria-hidden', 'true');
    return sep;
}

/**
 * Wrap static Markdown `<pre class="mermaid">` blocks inside `.m3-mermaid-figure.mermaid-blueprint`
 * figure containers with plain descriptive titles, per-diagram zoom/SVG/PNG/Expand toolbars, and
 * managed SVG hosts isolated from `astro-mermaid` theme-toggle overwrites.
 */
export function enhanceMarkdownMermaidBlocks(
    container: ParentNode,
    filenamePrefix = ''
): void {
    snapshotMermaidSources(container);

    const usedFilenameCounts = new Map<string, number>();
    const existingFigures = Array.from(
        container.querySelectorAll<HTMLElement>('figure.m3-mermaid-figure')
    );
    existingFigures.forEach((fig) => {
        const existingBase = fig.dataset.filenameBase;
        if (existingBase) {
            usedFilenameCounts.set(existingBase, (usedFilenameCounts.get(existingBase) ?? 0) + 1);
        }
    });

    const rawBlocks = Array.from(container.querySelectorAll<HTMLElement>('pre.mermaid'));
    rawBlocks.forEach((preEl, rawIdx) => {
        if (preEl.closest('figure.m3-mermaid-figure')) return;

        const figureIndex = existingFigures.length + rawIdx;
        const hasSvg = Boolean(preEl.querySelector('svg'));
        const attrSource = (preEl.getAttribute('data-diagram') || '').trim();
        const rawSource = attrSource || (!hasSvg ? (preEl.textContent || '').trim() : '');
        if (!rawSource || rawSource.startsWith('#mermaid-') || rawSource.includes('@keyframes')) {
            return;
        }

        const diagramTitle = resolveDiagramTitle(rawSource, preEl, figureIndex);
        const filenameBase = buildDiagramFilename(
            filenamePrefix,
            diagramTitle,
            figureIndex,
            usedFilenameCounts
        );

        const figure = document.createElement('figure');
        figure.className = 'm3-mermaid-figure mermaid-blueprint not-content';
        figure.setAttribute('data-blueprint-fig', String(figureIndex + 1));
        figure.setAttribute('data-zoom-container', 'true');
        figure.setAttribute('data-zoom-mode', 'svg');
        figure.dataset.diagramTitle = diagramTitle;
        figure.dataset.filenameBase = filenameBase;
        figure.setAttribute('aria-label', diagramTitle);

        const bar = document.createElement('div');
        bar.className = 'm3-mermaid-figure-bar mermaid-blueprint-bar';

        const caption = document.createElement('span');
        caption.className = 'm3-mermaid-figure-title mermaid-blueprint-title';
        caption.setAttribute('data-diagram-title', 'true');
        caption.textContent = diagramTitle;

        const toolbar = document.createElement('div');
        toolbar.className = 'm3-mermaid-toolbar mermaid-toolbar';
        toolbar.setAttribute('role', 'toolbar');
        toolbar.setAttribute('aria-label', `Controls for ${diagramTitle}`);

        const zoomOutBtn = makeBlueprintToolbarBtn('−', 'Zoom out diagram');
        zoomOutBtn.setAttribute('data-zoom-action', 'out');

        const zoomLabel = document.createElement('span');
        zoomLabel.className = 'mermaid-zoom-label';
        zoomLabel.setAttribute('data-zoom-label', 'true');
        zoomLabel.setAttribute('aria-live', 'polite');
        zoomLabel.textContent = '100%';

        const zoomInBtn = makeBlueprintToolbarBtn('+', 'Zoom in diagram');
        zoomInBtn.setAttribute('data-zoom-action', 'in');

        const resetBtn = makeBlueprintToolbarBtn('Reset', 'Reset zoom to 100%');
        resetBtn.setAttribute('data-zoom-action', 'reset');

        const svgBtn = makeBlueprintToolbarBtn('SVG', `Download SVG: ${diagramTitle}`);
        svgBtn.setAttribute('data-export-format', 'svg');

        const pngBtn = makeBlueprintToolbarBtn(
            'PNG',
            `Download high-resolution PNG: ${diagramTitle}`
        );
        pngBtn.setAttribute('data-export-format', 'png');

        const expandBtn = makeBlueprintToolbarBtn(
            'Expand',
            'Open diagram in fullscreen lightbox',
            'mermaid-blueprint-zoom'
        );
        expandBtn.setAttribute('data-expand-toggle', 'true');
        expandBtn.setAttribute('aria-expanded', 'false');

        toolbar.append(
            zoomOutBtn,
            zoomLabel,
            zoomInBtn,
            resetBtn,
            makeBlueprintSep(),
            svgBtn,
            pngBtn,
            makeBlueprintSep(),
            expandBtn
        );

        bar.append(caption, toolbar);

        const viewport = document.createElement('div');
        viewport.className = 'm3-mermaid-viewport mermaid-viewport';

        const zoomStage = document.createElement('div');
        zoomStage.className = 'm3-mermaid-zoom-stage mermaid-zoom-stage';
        zoomStage.setAttribute('data-zoom-target', 'true');

        const host = document.createElement('div');
        host.className = 'm3-mermaid-host';
        host.setAttribute('data-mermaid-managed', 'true');
        host.setAttribute('data-diagram', rawSource);
        host.innerHTML = '<p class="m3-diagram-loading">Rendering diagram...</p>';

        zoomStage.appendChild(host);
        viewport.appendChild(zoomStage);
        figure.append(bar, viewport);

        // Detach the original <pre class="mermaid"> so astro-mermaid cannot race/overwrite our host
        preEl.replaceWith(figure);

        bindDiagramExportButtons(figure, {
            getSvgContainer: () => host,
            getSource: () => host.getAttribute('data-diagram') || undefined,
            filenameBase: () => figure.dataset.filenameBase || filenameBase,
        });
        bindDiagramZoom(figure);
        bindDiagramExpand(figure);
    });
}

export interface RepairMermaidOptions {
    filenamePrefix?: string;
}

/**
 * Upgrade and re-render visible Markdown Mermaid blocks in a container (fixing hidden-tab layout,
 * injecting descriptive blueprint title bars + toolbars, theme-synced colors, and copyright watermarks).
 */
export async function repairVisibleMermaidBlocks(
    container: ParentNode,
    force = false,
    options: RepairMermaidOptions = {}
): Promise<void> {
    enhanceMarkdownMermaidBlocks(container, options.filenamePrefix || '');

    const activeTheme =
        typeof document !== 'undefined' &&
        document.documentElement.getAttribute('data-theme') === 'light'
            ? 'light'
            : 'dark';
    const hosts = Array.from(
        container.querySelectorAll<HTMLElement>(
            '.m3-mermaid-host[data-mermaid-managed="true"], pre.mermaid'
        )
    );
    for (const hostEl of hosts) {
        if (hostEl.closest('[hidden]')) continue;
        if (!force && !needsVisibleMermaidRepair(hostEl)) continue;

        const hasSvg = Boolean(hostEl.querySelector('svg'));
        const attrSource = (hostEl.getAttribute('data-diagram') || '').trim();
        const source = attrSource || (!hasSvg ? (hostEl.textContent || '').trim() : '');
        if (!source || source.startsWith('#mermaid-') || source.includes('@keyframes')) continue;
        if (!hostEl.hasAttribute('data-diagram')) {
            hostEl.setAttribute('data-diagram', source);
        }

        try {
            const svg = await renderMermaidSvg('md-dag', source);
            hostEl.innerHTML = svg;
            hostEl.setAttribute('data-processed', 'true');
            hostEl.dataset.archRenderedVisible = 'true';
            hostEl.dataset.archTheme = activeTheme;
            finalizeRenderedMermaidSvg(hostEl.querySelector('svg'));
        } catch (err) {
            console.error('Mermaid static block render failed:', err);
        }
    }
}

function collectZoomContainers(scope: ParentNode): HTMLElement[] {
    const boxes: HTMLElement[] = [];
    if (scope instanceof HTMLElement && scope.matches('[data-zoom-container="true"]')) {
        boxes.push(scope);
    }
    scope.querySelectorAll<HTMLElement>('[data-zoom-container="true"]').forEach((el) => {
        boxes.push(el);
    });
    return boxes;
}

/** Bind `- / 100% / + / reset` zoom buttons within `[data-zoom-container="true"]` containers. */
export function bindDiagramZoom(scope: ParentNode = document): void {
    collectZoomContainers(scope).forEach((box) => {
        if (box.dataset.zoomBound === 'true') return;
        box.dataset.zoomBound = 'true';

        const ownsEl = (el: Element) => el.closest('[data-zoom-container="true"]') === box;
        const target = Array.from(box.querySelectorAll<HTMLElement>('[data-zoom-target="true"]')).find(
            ownsEl
        );
        const label = Array.from(box.querySelectorAll<HTMLElement>('[data-zoom-label="true"]')).find(
            ownsEl
        );
        if (!target) return;

        const isSvgMode =
            box.dataset.zoomMode === 'svg' ||
            target.classList.contains('m3-diagram-canvas') ||
            target.classList.contains('m3-mermaid-zoom-stage');
        const viewport =
            target.closest<HTMLElement>('.mermaid-viewport, .m3-diagram-viewport') || box;

        let scale = 1;
        let refBaseWidth: number | null = null;

        const applyZoom = () => {
            if (label) label.textContent = `${Math.round(scale * 100)}%`;

            if (isSvgMode) {
                const svgEl = target.querySelector<SVGSVGElement>('svg');
                if (!svgEl) return;

                const { width: vbW, height: vbH } = getSvgDimensions(svgEl);
                const isExpanded = box.classList.contains('is-expanded');

                if (scale === 1) {
                    refBaseWidth = null;
                    if (isExpanded) {
                        const vw = Math.max(240, viewport.clientWidth - 24);
                        const vh = Math.max(200, viewport.clientHeight - 24);
                        const fitByHeightW = vbH > 0 ? (vh * vbW) / vbH : vw;
                        const expandedW = Math.min(
                            vw,
                            Math.max(Math.min(vbW, vw), Math.min(vbW * 1.45, vw, fitByHeightW))
                        );
                        svgEl.style.maxWidth = 'none';
                        svgEl.style.width = `${Math.round(expandedW)}px`;
                        svgEl.style.height = 'auto';
                    } else {
                        svgEl.style.width = '100%';
                        svgEl.style.maxWidth = vbW ? `min(100%, ${vbW}px)` : '100%';
                        svgEl.style.height = 'auto';
                    }
                    return;
                }

                if (!refBaseWidth) {
                    const rect = svgEl.getBoundingClientRect();
                    refBaseWidth = rect.width > 24 ? rect.width : vbW;
                }

                svgEl.style.maxWidth = 'none';
                svgEl.style.width = `${Math.max(160, Math.round(refBaseWidth * scale))}px`;
                svgEl.style.height = 'auto';
                return;
            }

            target.style.transform = scale === 1 ? '' : `scale(${scale})`;
            target.style.transformOrigin = 'top left';
        };

        box.addEventListener('atruss:sync-zoom', () => {
            refBaseWidth = null;
            applyZoom();
        });
        box.addEventListener('atruss:reset-zoom', () => {
            scale = 1;
            refBaseWidth = null;
            applyZoom();
        });

        Array.from(box.querySelectorAll<HTMLButtonElement>('[data-zoom-action]'))
            .filter(ownsEl)
            .forEach((btn) => {
                btn.addEventListener('click', () => {
                    const act = btn.dataset.zoomAction;
                    if (isSvgMode && scale === 1 && (act === 'in' || act === 'out')) {
                        const svgEl = target.querySelector<SVGSVGElement>('svg');
                        if (svgEl) {
                            refBaseWidth =
                                svgEl.getBoundingClientRect().width ||
                                getSvgDimensions(svgEl).width;
                        }
                    }
                    if (act === 'in') scale = Math.min(2.6, Number((scale + 0.2).toFixed(2)));
                    else if (act === 'out') scale = Math.max(0.5, Number((scale - 0.2).toFixed(2)));
                    else {
                        scale = 1;
                        refBaseWidth = null;
                    }
                    applyZoom();
                });
            });
    });
}

interface ExpandController {
    box: HTMLElement;
    collapse: () => void;
}

let sharedBackdrop: HTMLDivElement | null = null;
let activeExpandedController: ExpandController | null = null;
let lightboxListenersBound = false;

function ensureLightboxBackdrop(): HTMLDivElement {
    if (sharedBackdrop && document.body.contains(sharedBackdrop)) {
        return sharedBackdrop;
    }
    const existing = document.querySelector<HTMLDivElement>('.mermaid-lightbox-backdrop');
    if (existing) {
        sharedBackdrop = existing;
    } else {
        const backdrop = document.createElement('div');
        backdrop.className = 'mermaid-lightbox-backdrop';
        backdrop.hidden = true;
        backdrop.setAttribute('aria-hidden', 'true');
        document.body.appendChild(backdrop);
        sharedBackdrop = backdrop;
    }

    if (!lightboxListenersBound) {
        lightboxListenersBound = true;
        sharedBackdrop.addEventListener('click', () => {
            activeExpandedController?.collapse();
        });
        document.addEventListener('keydown', (e: KeyboardEvent) => {
            if (e.key === 'Escape' && activeExpandedController) {
                e.preventDefault();
                activeExpandedController.collapse();
            }
        });
    }
    return sharedBackdrop;
}

function updateExpandButtonState(btn: HTMLButtonElement, expanded: boolean): void {
    const icon = btn.querySelector<HTMLElement>('.material-symbols-outlined');
    if (icon) {
        icon.textContent = expanded ? 'close_fullscreen' : 'fullscreen';
    } else {
        btn.textContent = expanded ? 'Collapse' : 'Expand';
    }
    btn.setAttribute('aria-expanded', String(expanded));
    const titleText = expanded
        ? 'Exit fullscreen lightbox (Esc)'
        : 'Open diagram in fullscreen lightbox';
    btn.title = titleText;
    btn.setAttribute('aria-label', expanded ? 'Exit fullscreen lightbox' : titleText);
}

/** Bind fullscreen lightbox `Expand`/`Collapse` controls (`[data-expand-toggle="true"]`) with Esc/backdrop dismissal. */
export function bindDiagramExpand(scope: ParentNode = document): void {
    collectZoomContainers(scope).forEach((box) => {
        if (box.dataset.expandBound === 'true') return;
        const ownsEl = (el: Element) => el.closest('[data-zoom-container="true"]') === box;
        const expandBtn = Array.from(
            box.querySelectorAll<HTMLButtonElement>('[data-expand-toggle="true"]')
        ).find(ownsEl);
        if (!expandBtn) return;

        box.dataset.expandBound = 'true';
        const backdrop = ensureLightboxBackdrop();

        const controller: ExpandController = {
            box,
            collapse: () => {
                if (!box.classList.contains('is-expanded')) return;
                box.classList.remove('is-expanded');
                updateExpandButtonState(expandBtn, false);
                backdrop.hidden = true;
                document.body.style.overflow = '';
                if (activeExpandedController === controller) {
                    activeExpandedController = null;
                }
                box.dispatchEvent(new CustomEvent('atruss:reset-zoom'));
                expandBtn.focus();
            },
        };

        expandBtn.addEventListener('click', () => {
            if (box.classList.contains('is-expanded')) {
                controller.collapse();
                return;
            }
            if (activeExpandedController && activeExpandedController !== controller) {
                activeExpandedController.collapse();
            }
            // Clear any outer prose scale transform so fixed positioning anchors cleanly to the viewport
            const outerZoom = box.parentElement?.closest<HTMLElement>('[data-zoom-container="true"]');
            if (outerZoom) {
                outerZoom.dispatchEvent(new CustomEvent('atruss:reset-zoom'));
            }
            box.classList.add('is-expanded');
            updateExpandButtonState(expandBtn, true);
            backdrop.hidden = false;
            document.body.style.overflow = 'hidden';
            activeExpandedController = controller;
            window.requestAnimationFrame(() => {
                box.dispatchEvent(new CustomEvent('atruss:reset-zoom'));
            });
        });
    });
}

function triggerDownload(blob: Blob, filename: string): void {
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function serializeSvgElement(
    svgEl: SVGSVGElement
): { xml: string; width: number; height: number; surfaceBg: string } {
    const clone = svgEl.cloneNode(true) as SVGSVGElement;
    clone.setAttribute('xmlns', SVG_NS);
    clone.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink');

    const { width, height, surfaceBg } = applyCopyrightWatermarkToSvg(clone, {
        includeBackground: true,
    });
    clone.removeAttribute('data-base-viewbox');
    clone.setAttribute('width', String(width));
    clone.setAttribute('height', String(height));
    clone.style.maxWidth = 'none';
    clone.style.width = '';
    clone.style.height = '';
    clone.style.backgroundColor = surfaceBg;

    const serializer = new XMLSerializer();
    return { xml: serializer.serializeToString(clone), width, height, surfaceBg };
}

/** Download the rendered `<svg>` element inside a diagram container as a standalone watermarked SVG file. */
export function downloadSvgFromElement(containerEl: Element | null, filename: string): boolean {
    if (!containerEl) return false;
    const svgEl = containerEl.querySelector<SVGSVGElement>('svg');
    if (!svgEl) return false;

    const { xml } = serializeSvgElement(svgEl);
    const safeName = filename.endsWith('.svg') ? filename : `${filename}.svg`;
    triggerDownload(new Blob([xml], { type: 'image/svg+xml;charset=utf-8' }), safeName);
    return true;
}

/** Export a rendered diagram SVG as a 2x high-DPI watermarked PNG, falling back cleanly if tainted by foreignObject. */
export async function exportSvgToPng(
    containerEl: Element | null,
    filename: string,
    diagramSource?: string,
    scale = 2
): Promise<boolean> {
    if (!containerEl) return false;
    const liveSvg = containerEl.querySelector<SVGSVGElement>('svg');
    if (!liveSvg) return false;

    let targetSvg: SVGSVGElement = liveSvg;
    let tempHost: HTMLDivElement | null = null;

    if (liveSvg.querySelector('foreignObject') && diagramSource) {
        try {
            const cleanMarkup = await renderMermaidSvg('png-export', diagramSource, false);
            tempHost = document.createElement('div');
            tempHost.style.position = 'fixed';
            tempHost.style.left = '-99999px';
            tempHost.style.top = '0';
            tempHost.innerHTML = cleanMarkup;
            document.body.appendChild(tempHost);
            const cleanSvg = tempHost.querySelector<SVGSVGElement>('svg');
            if (cleanSvg) targetSvg = cleanSvg;
        } catch (err) {
            console.warn('Re-render without htmlLabels failed during PNG export:', err);
        }
    }

    try {
        const { xml, width, height, surfaceBg } = serializeSvgElement(targetSvg);
        const safeName = filename.endsWith('.png') ? filename : `${filename}.png`;
        const dataUrl = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(xml)}`;

        const img = new Image();
        await new Promise<void>((resolve, reject) => {
            img.onload = () => resolve();
            img.onerror = (ev) => reject(ev);
            img.src = dataUrl;
        });

        const effectiveScale = Math.min(
            scale,
            8192 / Math.max(1, width),
            8192 / Math.max(1, height)
        );
        const canvas = document.createElement('canvas');
        canvas.width = Math.max(1, Math.round(width * effectiveScale));
        canvas.height = Math.max(1, Math.round(height * effectiveScale));

        const ctx = canvas.getContext('2d');
        if (!ctx) return false;

        ctx.fillStyle = surfaceBg;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

        const pngBlob = await new Promise<Blob | null>((resolve) => {
            try {
                canvas.toBlob((blob) => resolve(blob), 'image/png');
            } catch {
                resolve(null);
            }
        });

        if (pngBlob) {
            triggerDownload(pngBlob, safeName);
            return true;
        }

        // SecurityError taint fallback: try DataURL or fallback to SVG download
        try {
            const pngUrl = canvas.toDataURL('image/png');
            const res = await fetch(pngUrl);
            triggerDownload(await res.blob(), safeName);
            return true;
        } catch {
            return downloadSvgFromElement(containerEl, filename.replace(/\.png$/i, ''));
        }
    } catch (err) {
        console.warn('PNG rasterization failed, falling back to SVG:', err);
        return downloadSvgFromElement(containerEl, filename.replace(/\.png$/i, ''));
    } finally {
        if (tempHost) tempHost.remove();
    }
}

export interface DiagramExportOptions {
    getSvgContainer: () => Element | null;
    getSource?: () => string | undefined;
    filenameBase: string | (() => string);
}

/** Bind SVG and PNG download buttons (`[data-export-format]`) within a diagram card. */
export function bindDiagramExportButtons(scope: ParentNode, opts: DiagramExportOptions): void {
    const scopeZoomBox =
        scope instanceof HTMLElement && scope.matches('[data-zoom-container="true"]')
            ? scope
            : null;

    scope.querySelectorAll<HTMLButtonElement>('[data-export-format]').forEach((btn) => {
        if (scopeZoomBox && btn.closest('[data-zoom-container="true"]') !== scopeZoomBox) {
            return;
        }
        if (btn.dataset.exportBound === 'true') return;
        btn.dataset.exportBound = 'true';

        btn.addEventListener('click', async () => {
            const fmt = (btn.dataset.exportFormat || 'svg').toLowerCase();
            const container = opts.getSvgContainer();
            if (!container) return;

            const resolvedBase =
                typeof opts.filenameBase === 'function' ? opts.filenameBase() : opts.filenameBase;

            if (fmt === 'png') {
                btn.disabled = true;
                try {
                    await exportSvgToPng(container, resolvedBase, opts.getSource?.());
                } finally {
                    btn.disabled = false;
                }
            } else {
                downloadSvgFromElement(container, resolvedBase);
            }
        });
    });
}
