import mermaid from 'mermaid';
import elkLayouts from '@mermaid-js/layout-elk';

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
    const rawMax = svgEl.style.maxWidth;
    if (rawMax && rawMax !== '100%' && !rawMax.startsWith('min(')) {
        svgEl.style.maxWidth = `min(100%, ${rawMax})`;
    } else if (!rawMax) {
        svgEl.style.maxWidth = '100%';
    }
    svgEl.style.width = '100%';
    svgEl.style.height = 'auto';
    svgEl.style.display = 'block';
    svgEl.style.margin = '0 auto';
}

/** Check whether an existing Mermaid SVG failed layout or was rendered for a different theme. */
export function needsVisibleMermaidRepair(preEl: HTMLElement): boolean {
    const activeTheme =
        typeof document !== 'undefined' &&
        document.documentElement.getAttribute('data-theme') === 'light'
            ? 'light'
            : 'dark';
    if (preEl.dataset.archRenderedVisible === 'true' && preEl.dataset.archTheme === activeTheme) {
        return false;
    }
    if (preEl.dataset.archTheme !== activeTheme) return true;
    const svgEl = preEl.querySelector<SVGSVGElement>('svg');
    if (!svgEl) return true;
    const vb = (svgEl.getAttribute('viewBox') || '').trim();
    if (vb === '-8 -8 16 16') return true;
    const rect = svgEl.getBoundingClientRect();
    return rect.width <= 24 || rect.height <= 24;
}

/** Snapshot raw Mermaid source into `data-diagram` before any renderer replaces it with SVG. */
export function snapshotMermaidSources(scope: ParentNode = document): void {
    scope.querySelectorAll<HTMLElement>('pre.mermaid').forEach((preEl) => {
        if (preEl.hasAttribute('data-diagram')) return;
        if (preEl.querySelector('svg')) return;
        const raw = (preEl.textContent || '').trim();
        if (raw && !raw.startsWith('#mermaid-') && !raw.includes('@keyframes')) {
            preEl.setAttribute('data-diagram', raw);
        }
    });
}

/** Re-render visible `<pre class="mermaid">` blocks in a container (fixing hidden-tab & theme contrast). */
export async function repairVisibleMermaidBlocks(
    container: ParentNode,
    force = false
): Promise<void> {
    snapshotMermaidSources(container);

    const activeTheme =
        typeof document !== 'undefined' &&
        document.documentElement.getAttribute('data-theme') === 'light'
            ? 'light'
            : 'dark';
    const blocks = Array.from(container.querySelectorAll<HTMLElement>('pre.mermaid'));
    for (const preEl of blocks) {
        if (preEl.closest('[hidden]')) continue;
        if (!force && !needsVisibleMermaidRepair(preEl)) continue;

        const hasSvg = Boolean(preEl.querySelector('svg'));
        const attrSource = (preEl.getAttribute('data-diagram') || '').trim();
        const source = attrSource || (!hasSvg ? (preEl.textContent || '').trim() : '');
        if (!source || source.startsWith('#mermaid-') || source.includes('@keyframes')) continue;
        if (!preEl.hasAttribute('data-diagram')) {
            preEl.setAttribute('data-diagram', source);
        }

        try {
            const svg = await renderMermaidSvg('md-dag', source);
            preEl.innerHTML = svg;
            preEl.setAttribute('data-processed', 'true');
            preEl.dataset.archRenderedVisible = 'true';
            preEl.dataset.archTheme = activeTheme;
            applyResponsiveSvgStyle(preEl.querySelector('svg'));
        } catch (err) {
            console.error('Mermaid static block render failed:', err);
        }
    }
}

/** Bind `- / 100% / + / reset` zoom buttons within `[data-zoom-container="true"]` containers. */
export function bindDiagramZoom(scope: ParentNode = document): void {
    scope.querySelectorAll<HTMLElement>('[data-zoom-container="true"]').forEach((box) => {
        if (box.dataset.zoomBound === 'true') return;
        box.dataset.zoomBound = 'true';
        const target = box.querySelector<HTMLElement>('[data-zoom-target="true"]');
        const label = box.querySelector<HTMLElement>('[data-zoom-label="true"]');
        if (!target) return;

        let scale = 1;
        const update = () => {
            target.style.transform = `scale(${scale})`;
            target.style.transformOrigin = 'top left';
            if (label) label.textContent = `${Math.round(scale * 100)}%`;
        };

        box.querySelectorAll<HTMLButtonElement>('[data-zoom-action]').forEach((btn) => {
            btn.addEventListener('click', () => {
                const act = btn.dataset.zoomAction;
                if (act === 'in') scale = Math.min(2.2, +(scale + 0.15).toFixed(2));
                else if (act === 'out') scale = Math.max(0.5, +(scale - 0.15).toFixed(2));
                else scale = 1;
                update();
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

function serializeSvgElement(svgEl: SVGSVGElement): { xml: string; width: number; height: number } {
    const clone = svgEl.cloneNode(true) as SVGSVGElement;
    clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    clone.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink');

    let width = 1200;
    let height = 800;
    const vbAttr = (svgEl.getAttribute('viewBox') || '').trim();
    const vbParts = vbAttr.split(/[\s,]+/).map(Number);
    if (vbParts.length === 4 && Number.isFinite(vbParts[2]) && vbParts[2] > 0 && Number.isFinite(vbParts[3]) && vbParts[3] > 0) {
        width = Math.ceil(vbParts[2]);
        height = Math.ceil(vbParts[3]);
    } else {
        const rect = svgEl.getBoundingClientRect();
        if (rect.width > 16 && rect.height > 16) {
            width = Math.ceil(rect.width);
            height = Math.ceil(rect.height);
        }
    }

    clone.setAttribute('width', String(width));
    clone.setAttribute('height', String(height));
    clone.style.maxWidth = 'none';

    const serializer = new XMLSerializer();
    return { xml: serializer.serializeToString(clone), width, height };
}

/** Download the rendered `<svg>` element inside a diagram container as an SVG file. */
export function downloadSvgFromElement(containerEl: Element | null, filename: string): boolean {
    if (!containerEl) return false;
    const svgEl = containerEl.querySelector<SVGSVGElement>('svg');
    if (!svgEl) return false;

    const { xml } = serializeSvgElement(svgEl);
    const safeName = filename.endsWith('.svg') ? filename : `${filename}.svg`;
    triggerDownload(new Blob([xml], { type: 'image/svg+xml;charset=utf-8' }), safeName);
    return true;
}

/** Export a rendered diagram SVG as a 2x high-DPI PNG, falling back cleanly if tainted by foreignObject. */
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
        const { xml, width, height } = serializeSvgElement(targetSvg);
        const safeName = filename.endsWith('.png') ? filename : `${filename}.png`;
        const dataUrl = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(xml)}`;

        const img = new Image();
        await new Promise<void>((resolve, reject) => {
            img.onload = () => resolve();
            img.onerror = (ev) => reject(ev);
            img.src = dataUrl;
        });

        const canvas = document.createElement('canvas');
        canvas.width = Math.max(1, Math.min(8192, Math.round(width * scale)));
        canvas.height = Math.max(1, Math.min(8192, Math.round(height * scale)));

        const ctx = canvas.getContext('2d');
        if (!ctx) return false;

        const isLight = document.documentElement.getAttribute('data-theme') === 'light';
        const computedBg = getComputedStyle(document.documentElement)
            .getPropertyValue('--md-sys-color-surface-container-lowest')
            .trim();
        ctx.fillStyle = computedBg || (isLight ? '#ffffff' : '#0a0e14');
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
    filenameBase: string;
}

/** Bind SVG and PNG download buttons (`[data-export-format]`) within a diagram card. */
export function bindDiagramExportButtons(scope: ParentNode, opts: DiagramExportOptions): void {
    scope.querySelectorAll<HTMLButtonElement>('[data-export-format]').forEach((btn) => {
        if (btn.dataset.exportBound === 'true') return;
        btn.dataset.exportBound = 'true';

        btn.addEventListener('click', async () => {
            const fmt = (btn.dataset.exportFormat || 'svg').toLowerCase();
            const container = opts.getSvgContainer();
            if (!container) return;

            if (fmt === 'png') {
                await exportSvgToPng(container, opts.filenameBase, opts.getSource?.());
            } else {
                downloadSvgFromElement(container, opts.filenameBase);
            }
        });
    });
}
