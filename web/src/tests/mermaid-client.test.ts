import assert from 'node:assert/strict';
import {
  COPYRIGHT_WATERMARK_TEXT,
  SVG_NS,
  applyCopyrightWatermarkToSvg,
  buildDiagramFilename,
  resolveDiagramTitle,
  slugifySegment,
} from '../lib/diagram-metadata.ts';

class MockElement {
  tagName: string;
  namespaceURI: string | null;
  attrs = new Map<string, string>();
  children: MockElement[] = [];
  parent: MockElement | null = null;
  textContent = '';
  ownerDocument: MockDocument;

  constructor(doc: MockDocument, tagName: string, ns: string | null = null) {
    this.ownerDocument = doc;
    this.tagName = tagName;
    this.namespaceURI = ns;
  }

  get firstChild(): MockElement | null {
    return this.children[0] ?? null;
  }

  setAttribute(name: string, value: string): void {
    this.attrs.set(name, String(value));
  }

  getAttribute(name: string): string | null {
    return this.attrs.has(name) ? (this.attrs.get(name) ?? null) : null;
  }

  hasAttribute(name: string): boolean {
    return this.attrs.has(name);
  }

  appendChild(child: MockElement): MockElement {
    child.parent = this;
    this.children.push(child);
    return child;
  }

  insertBefore(child: MockElement, ref: MockElement | null): MockElement {
    child.parent = this;
    if (!ref) {
      this.children.push(child);
      return child;
    }
    const idx = this.children.indexOf(ref);
    if (idx === -1) this.children.push(child);
    else this.children.splice(idx, 0, child);
    return child;
  }

  remove(): void {
    if (!this.parent) return;
    const idx = this.parent.children.indexOf(this);
    if (idx !== -1) this.parent.children.splice(idx, 1);
    this.parent = null;
  }

  private matchesSimpleSelector(selector: string): boolean {
    const trimmed = selector.trim();
    const attrMatch = trimmed.match(/^\[([a-zA-Z0-9_-]+)\]$/);
    if (attrMatch) return this.hasAttribute(attrMatch[1]);
    return this.tagName.toLowerCase() === trimmed.toLowerCase();
  }

  querySelectorAll(selectorList: string): MockElement[] {
    const selectors = selectorList.split(',').map((s) => s.trim()).filter(Boolean);
    const matches: MockElement[] = [];
    const visit = (node: MockElement) => {
      for (const child of node.children) {
        if (selectors.some((sel) => child.matchesSimpleSelector(sel))) {
          matches.push(child);
        }
        visit(child);
      }
    };
    visit(this);
    return matches;
  }
}

class MockDocument {
  documentElement: MockElement;

  constructor(theme: 'dark' | 'light' = 'dark') {
    this.documentElement = new MockElement(this, 'html');
    this.documentElement.setAttribute('data-theme', theme);
  }

  createElementNS(ns: string, tagName: string): MockElement {
    return new MockElement(this, tagName, ns);
  }
}

function testCopyrightWatermarkConstant(): void {
  const year = new Date().getFullYear();
  assert.equal(
    COPYRIGHT_WATERMARK_TEXT,
    `© ${year} Shashi Kumar · kumarshaz.github.io`,
    'Watermark constant must match kumarshaz.github.io format'
  );
}

function testResolveDiagramTitlePrecedence(): void {
  // 1. Explicit %% title: takes highest priority
  const withComment = [
    'flowchart TD',
    '  %% title: Building Block View — fastapi/fastapi',
    '  accTitle: Ignored Accessibility Title',
    '  A --> B',
  ].join('\n');
  assert.equal(resolveDiagramTitle(withComment), 'Building Block View — fastapi/fastapi');

  // 2. accTitle: takes priority over YAML frontmatter and native titles
  const withAccTitle = [
    '---',
    'title: "Ignored YAML Title"',
    '---',
    'flowchart LR',
    '  accTitle: Clean-Core Sidecar Interaction',
    '  A --> B',
  ].join('\n');
  assert.equal(resolveDiagramTitle(withAccTitle), 'Clean-Core Sidecar Interaction');

  // 3. YAML frontmatter title
  const withYamlTitle = [
    '---',
    'title: "System Boundary Map"',
    'config:',
    '  layout: elk',
    '---',
    'flowchart TB',
    '  A --> B',
  ].join('\n');
  assert.equal(resolveDiagramTitle(withYamlTitle), 'System Boundary Map');

  // 4. Native title statement in timeline / gantt / pie / journey / xychart-beta
  const timelineSrc = [
    'timeline',
    '  title Release Train Cadence',
    '  2026 : GA',
  ].join('\n');
  assert.equal(resolveDiagramTitle(timelineSrc), 'Release Train Cadence');

  // 5. Mindmap root(...) label normalization
  const mindmapSrc = [
    'mindmap',
    '  root(("Engineering<br/>Atlas"))',
    '    Services',
  ].join('\n');
  assert.equal(resolveDiagramTitle(mindmapSrc), 'Engineering Atlas');

  // 6. Nearest preceding Markdown heading stripping Section N: / 1. / A. prefixes
  const headings = [
    { textContent: '1. Building Block View', pos: 4 },
    { textContent: 'Section 7: Code-to-Cloud Deployment Traceability', pos: 4 },
    { textContent: 'Section 8: Later Heading', pos: 2 },
  ];
  const mockProse = {
    querySelectorAll: () =>
      headings.map((h) => ({
        textContent: h.textContent,
        compareDocumentPosition: () => h.pos,
      })),
  };
  const mockPre = {
    closest: (sel: string) => (sel.includes('.markdown-content') ? mockProse : null),
  } as unknown as Element;
  assert.equal(
    resolveDiagramTitle('flowchart LR\n  A --> B', mockPre, 1),
    'Code-to-Cloud Deployment Traceability'
  );

  // 7. Fallback title and neutral Figure N
  assert.equal(
    resolveDiagramTitle('flowchart TD\n  A --> B', null, 2, 'Custom Fallback'),
    'Custom Fallback'
  );
  assert.equal(resolveDiagramTitle('flowchart TD\n  A --> B', null, 2), 'Figure 3');
}

function testSlugifyAndFilenameBuilder(): void {
  assert.equal(slugifySegment('Code → Cloud & Security'), 'code-to-cloud-and-security');

  // Prefix deduplication before 48-char title truncation
  assert.equal(
    buildDiagramFilename(
      'kumarshaz-atruss-code-atlas',
      'kumarshaz/atruss-code-atlas — Module Architecture Tree'
    ),
    'kumarshaz-atruss-code-atlas-module-architecture-tree'
  );

  // Long org/repo prefix does not truncate descriptive suffix prematurely
  assert.equal(
    buildDiagramFilename(
      'very-long-organization-name-enterprise-monorepo-service',
      'very-long-organization-name/enterprise-monorepo-service — CI/CD Verification Job Dependency DAG'
    ),
    'very-long-organization-name-enterprise-monorepo-service-ci-cd-verification-job-dependency-dag'
  );

  // Collision suffixing via usedCounts map
  const used = new Map<string, number>();
  assert.equal(
    buildDiagramFilename('fastapi-fastapi', 'Building Block View', 0, used),
    'fastapi-fastapi-building-block-view'
  );
  assert.equal(
    buildDiagramFilename('fastapi-fastapi', 'Building Block View', 1, used),
    'fastapi-fastapi-building-block-view-2'
  );
  assert.equal(
    buildDiagramFilename('fastapi-fastapi', 'Building Block View', 2, used),
    'fastapi-fastapi-building-block-view-3'
  );

  // Empty prefix (CrossRepoTopology)
  assert.equal(
    buildDiagramFilename('', 'Cross-Repository Topology & Shared Dependencies'),
    'cross-repository-topology-and-shared-dependencie'
  );
}

function testApplyCopyrightWatermarkLiveExportAndIdempotency(): void {
  const darkDoc = new MockDocument('dark');
  const svg = darkDoc.createElementNS(SVG_NS, 'svg');
  svg.setAttribute('viewBox', '0 0 800 400');
  svg.setAttribute('height', '400');
  const contentGroup = darkDoc.createElementNS(SVG_NS, 'g');
  svg.appendChild(contentGroup);

  // Live render: no background rect, watermark group injected, viewBox expanded vertically
  const liveResult = applyCopyrightWatermarkToSvg(svg as unknown as SVGSVGElement, {
    includeBackground: false,
  });
  assert.equal(svg.getAttribute('data-base-viewbox'), '0 0 800 400');
  assert.equal(liveResult.width, 800);
  assert.ok(liveResult.height > 400, 'Watermark strip must expand SVG height');
  assert.equal(liveResult.surfaceBg, '#0a0e14');
  assert.equal(svg.querySelectorAll('[data-export-bg]').length, 0);

  const wmGroups = svg.querySelectorAll('[data-copyright-watermark]');
  assert.equal(wmGroups.length, 1);
  const wmLines = wmGroups[0].querySelectorAll('line');
  const wmTexts = wmGroups[0].querySelectorAll('text');
  assert.equal(wmLines.length, 2, 'Watermark must contain rule line and accent tick');
  assert.equal(wmTexts.length, 1, 'Watermark must contain copyright text node');
  assert.equal(wmTexts[0].textContent, COPYRIGHT_WATERMARK_TEXT);
  assert.equal(wmTexts[0].getAttribute('text-anchor'), 'end');
  assert.equal(svg.getAttribute('height'), String(liveResult.height));

  // Idempotent re-application on export with Light theme + embedded background
  darkDoc.documentElement.setAttribute('data-theme', 'light');
  const exportResult = applyCopyrightWatermarkToSvg(svg as unknown as SVGSVGElement, {
    includeBackground: true,
  });
  assert.equal(
    exportResult.height,
    liveResult.height,
    'Re-applying watermark must reuse data-base-viewbox without double expansion'
  );
  assert.equal(exportResult.surfaceBg, '#ffffff');
  assert.equal(svg.querySelectorAll('[data-copyright-watermark]').length, 1);
  const bgRects = svg.querySelectorAll('[data-export-bg]');
  assert.equal(bgRects.length, 1, 'Standalone export must embed background rect');
  assert.equal(svg.firstChild, bgRects[0], 'Background rect must be inserted as first child');
  assert.equal(bgRects[0].getAttribute('fill'), '#ffffff');
}

function testNarrowSvgHorizontalCentering(): void {
  const doc = new MockDocument('dark');
  const svg = doc.createElementNS(SVG_NS, 'svg');
  svg.setAttribute('viewBox', '0 0 140 200');
  svg.setAttribute('height', '100%');

  const res = applyCopyrightWatermarkToSvg(svg as unknown as SVGSVGElement, {
    includeBackground: false,
  });
  const [outX, outY, outW, outH] = (svg.getAttribute('viewBox') || '').split(/\s+/).map(Number);

  assert.ok(outW > 140, 'Narrow SVG viewBox must widen to fit watermark cleanly');
  assert.ok(outX < 0, 'Narrow SVG viewBox must shift left to center artwork above watermark');
  assert.equal(outY, 0);
  assert.ok(outH > 200);
  assert.equal(res.width, Math.ceil(outW));
  assert.equal(svg.getAttribute('height'), '100%', 'Percentage height attribute must remain untouched');
}

testCopyrightWatermarkConstant();
testResolveDiagramTitlePrecedence();
testSlugifyAndFilenameBuilder();
testApplyCopyrightWatermarkLiveExportAndIdempotency();
testNarrowSvgHorizontalCentering();
console.log('Mermaid copyright watermark & descriptive diagram title unit tests passed.');
