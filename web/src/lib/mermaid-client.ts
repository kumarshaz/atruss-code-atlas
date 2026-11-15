import mermaid from 'mermaid';

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

/** Configure Mermaid with theme-aware dark/light styling and safe size caps. */
export function configureMermaid(htmlLabels = true): void {
    const isDark = document.documentElement.getAttribute('data-theme') !== 'light';
    mermaid.initialize({
        startOnLoad: false,
        theme: isDark ? 'dark' : 'default',
        maxTextSize: 200000,
        flowchart: {
            useMaxWidth: true,
            htmlLabels,
            nodeSpacing: 28,
            rankSpacing: 44,
        },
    });
}

/** Render a Mermaid definition string into SVG markup using the active theme. */
export async function renderMermaidSvg(
    prefix: string,
    graphDef: string,
    htmlLabels = true
): Promise<string> {
    configureMermaid(htmlLabels);
    const renderId = `${safeId(prefix)}-${Math.random().toString(36).slice(2, 10)}`;
    const { svg } = await mermaid.render(renderId, graphDef);
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

/** Check whether an existing Mermaid SVG failed layout due to hidden-container rendering. */
export function needsVisibleMermaidRepair(preEl: HTMLElement): boolean {
    if (preEl.dataset.archRenderedVisible === 'true') return false;
    const svgEl = preEl.querySelector<SVGSVGElement>('svg');
    if (!svgEl) return true;
    const vb = (svgEl.getAttribute('viewBox') || '').trim();
    if (vb === '-8 -8 16 16') return true;
    const rect = svgEl.getBoundingClientRect();
    return rect.width <= 24 || rect.height <= 24;
}

/** Re-render visible `<pre class="mermaid">` blocks in a container (fixing hidden-tab 16x16 SVGs). */
export async function repairVisibleMermaidBlocks(
    container: ParentNode,
    force = false
): Promise<void> {
    const blocks = Array.from(container.querySelectorAll<HTMLElement>('pre.mermaid'));
    for (const preEl of blocks) {
        if (preEl.closest('[hidden]')) continue;
        if (!force && !needsVisibleMermaidRepair(preEl)) continue;

        const source =
            preEl.getAttribute('data-diagram') || (preEl.textContent || '').trim();
        if (!source) continue;
        if (!preEl.hasAttribute('data-diagram')) {
            preEl.setAttribute('data-diagram', source);
        }

        try {
            const svg = await renderMermaidSvg('md-dag', source);
            preEl.innerHTML = svg;
            preEl.setAttribute('data-processed', 'true');
            preEl.dataset.archRenderedVisible = 'true';
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
