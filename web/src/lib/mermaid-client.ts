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
export function configureMermaid(): void {
    const isDark = document.documentElement.getAttribute('data-theme') !== 'light';
    mermaid.initialize({
        startOnLoad: false,
        theme: isDark ? 'dark' : 'default',
        maxTextSize: 200000,
        flowchart: {
            useMaxWidth: true,
            htmlLabels: true,
            nodeSpacing: 28,
            rankSpacing: 44,
        },
    });
}

/** Render a Mermaid definition string into SVG markup using the active theme. */
export async function renderMermaidSvg(prefix: string, graphDef: string): Promise<string> {
    configureMermaid();
    const renderId = `${safeId(prefix)}-${Math.random().toString(36).slice(2, 10)}`;
    const { svg } = await mermaid.render(renderId, graphDef);
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
