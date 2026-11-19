import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

function normalizeSlug(segment) {
  return String(segment || '')
    .trim()
    .toLowerCase()
    .replace(/^\.+/, '');
}

function testSlugAndBasePathFormatting() {
  assert.equal(normalizeSlug('.NET'), 'net');
  assert.equal(normalizeSlug('fastapi'), 'fastapi');
  assert.equal(normalizeSlug('Azure-Samples'), 'azure-samples');

  const withBase = (baseUrl, p) => {
    const cleanBase = (baseUrl || '/').replace(/\/$/, '');
    return `${cleanBase}${p.startsWith('/') ? p : '/' + p}`;
  };

  assert.equal(withBase('/', '/orgs/'), '/orgs/');
  assert.equal(withBase('/atruss-code-atlas/', '/orgs/'), '/atruss-code-atlas/orgs/');
  assert.equal(
    withBase('/atruss-code-atlas', '/reports/fastapi/fastapi/'),
    '/atruss-code-atlas/reports/fastapi/fastapi/'
  );
}

function testM3ComponentsAndTokensPresent() {
  const themePath = path.resolve(process.cwd(), 'src/styles/material-theme.css');
  assert.ok(fs.existsSync(themePath), 'material-theme.css must exist');
  const css = fs.readFileSync(themePath, 'utf8');
  assert.ok(css.includes('--md-sys-color-primary'), 'Dark/Light M3 primary token missing');
  assert.ok(css.includes(":root[data-theme='light']"), 'Light theme override missing');

  const gridPath = path.resolve(process.cwd(), 'src/components/RepoGrid.astro');
  const gridSrc = fs.readFileSync(gridPath, 'utf8');
  assert.ok(gridSrc.includes('data-filter-chip'), 'M3 filter chips missing from RepoGrid.astro');
  assert.ok(gridSrc.includes('tier_1'), 'Tier 1 filter chip missing from RepoGrid.astro');
}

function testUiLayoutAndDiagramTraversalContracts() {
  const summarySrc = fs.readFileSync(
    path.resolve(process.cwd(), 'src/components/AtlasSummary.astro'),
    'utf8'
  );
  assert.ok(
    !summarySrc.includes('Material Design 3 Architecture Observatory'),
    'Deprecated observatory label must be removed from AtlasSummary.astro'
  );

  const astroConfigSrc = fs.readFileSync(path.resolve(process.cwd(), 'astro.config.mjs'), 'utf8');
  assert.ok(
    astroConfigSrc.includes('tableOfContents: false'),
    'Right-side TOC pane must be disabled via tableOfContents: false'
  );

  const cssSrc = fs.readFileSync(
    path.resolve(process.cwd(), 'src/styles/material-theme.css'),
    'utf8'
  );
  assert.ok(
    cssSrc.includes('--sl-content-width: 68rem'),
    'Expanded Starlight content width token required to prevent /orgs/ table cutoff'
  );

  const pipelineSrc = fs.readFileSync(
    path.resolve(process.cwd(), 'src/components/PipelineView.astro'),
    'utf8'
  );
  assert.ok(pipelineSrc.includes('flowchart TD'), 'PipelineView must render top-down (TD) DAGs');
  assert.ok(
    pipelineSrc.includes("closest('[hidden]')"),
    'PipelineView must defer Mermaid rendering while panel is hidden'
  );
  assert.ok(
    pipelineSrc.includes('atruss:tab-activated'),
    'PipelineView must listen for tab activation to render safely'
  );

  const archSrc = fs.readFileSync(
    path.resolve(process.cwd(), 'src/components/ArchitectureView.astro'),
    'utf8'
  );
  assert.ok(
    archSrc.includes('data-arch-root'),
    'ArchitectureView must mount interactive top-level module tree navigator'
  );
  assert.ok(
    archSrc.includes('repairVisibleMermaidBlocks'),
    'ArchitectureView must re-render hidden-tab Markdown Mermaid blocks once visible'
  );
  assert.ok(
    archSrc.includes('data-export-format="svg"'),
    'ArchitectureView must expose SVG export button'
  );
  assert.ok(
    archSrc.includes('data-export-format="png"'),
    'ArchitectureView must expose PNG export button'
  );
}

function testHorizon2UiComponentsAndContracts() {
  const mermaidSrc = fs.readFileSync(
    path.resolve(process.cwd(), 'src/lib/mermaid-client.ts'),
    'utf8'
  );
  assert.ok(mermaidSrc.includes('downloadSvgFromElement'), 'mermaid-client.ts must export SVG downloader');
  assert.ok(mermaidSrc.includes('exportSvgToPng'), 'mermaid-client.ts must export PNG exporter');
  assert.ok(mermaidSrc.includes('htmlLabels'), 'mermaid-client.ts must handle htmlLabels fallback for foreignObject');

  const tabsSrc = fs.readFileSync(
    path.resolve(process.cwd(), 'src/components/RepoTabs.astro'),
    'utf8'
  );
  assert.ok(tabsSrc.includes('data-m3-tab="scorecard"'), 'RepoTabs.astro must expose 4th scorecard tab');
  assert.ok(tabsSrc.includes('slot name="scorecard"'), 'RepoTabs.astro must render scorecard slot');
  assert.ok(tabsSrc.includes('data-m3-print="true"'), 'RepoTabs.astro must expose Print / Save PDF button');

  const scorecardPath = path.resolve(process.cwd(), 'src/components/ScorecardHeatmap.astro');
  assert.ok(fs.existsSync(scorecardPath), 'ScorecardHeatmap.astro must exist');
  const scorecardSrc = fs.readFileSync(scorecardPath, 'utf8');
  assert.ok(scorecardSrc.includes('m3-scorecard-hero'), 'ScorecardHeatmap must render scorecard hero');
  assert.ok(scorecardSrc.includes('m3-heatmap-grid'), 'ScorecardHeatmap must render complexity heatmap');

  const crossTopoPath = path.resolve(process.cwd(), 'src/components/CrossRepoTopology.astro');
  assert.ok(fs.existsSync(crossTopoPath), 'CrossRepoTopology.astro must exist');
  const crossTopoSrc = fs.readFileSync(crossTopoPath, 'utf8');
  assert.ok(crossTopoSrc.includes('flowchart TD'), 'CrossRepoTopology must use flowchart TD');

  const leaderboardSrc = fs.readFileSync(
    path.resolve(process.cwd(), 'src/components/LeaderboardView.astro'),
    'utf8'
  );
  assert.ok(leaderboardSrc.includes('CrossRepoTopology'), 'LeaderboardView must mount CrossRepoTopology');

  const cssSrc = fs.readFileSync(
    path.resolve(process.cwd(), 'src/styles/material-theme.css'),
    'utf8'
  );
  assert.ok(cssSrc.includes('@media print'), 'material-theme.css must define @media print rules');
  assert.ok(cssSrc.includes('.m3-tab-panel[hidden]'), '@media print must reveal hidden tab panels');

  const stubGenSrc = fs.readFileSync(
    path.resolve(process.cwd(), '../scripts/generate-report-stubs.py'),
    'utf8'
  );
  assert.ok(stubGenSrc.length > 0, 'generate-report-stubs.py must exist');
}

function testMermaidWatermarkAndTitleContracts() {
  const metadataSrc = fs.readFileSync(
    path.resolve(process.cwd(), 'src/lib/diagram-metadata.ts'),
    'utf8'
  );
  assert.ok(
    metadataSrc.includes('Shashi Kumar · kumarshaz.github.io'),
    'diagram-metadata.ts must define the canonical copyright watermark text'
  );
  assert.ok(
    metadataSrc.includes('applyCopyrightWatermarkToSvg'),
    'diagram-metadata.ts must export applyCopyrightWatermarkToSvg'
  );
  assert.ok(
    metadataSrc.includes('data-copyright-watermark'),
    'diagram-metadata.ts must tag injected watermark groups with data-copyright-watermark'
  );
  assert.ok(
    metadataSrc.includes('data-base-viewbox'),
    'diagram-metadata.ts must preserve data-base-viewbox for idempotent re-watermarking'
  );
  assert.ok(
    metadataSrc.includes('data-export-bg'),
    'diagram-metadata.ts must embed data-export-bg for standalone exports'
  );
  assert.ok(
    metadataSrc.includes('resolveDiagramTitle'),
    'diagram-metadata.ts must export resolveDiagramTitle'
  );
  assert.ok(
    metadataSrc.includes('buildDiagramFilename'),
    'diagram-metadata.ts must export buildDiagramFilename'
  );

  const mermaidSrc = fs.readFileSync(
    path.resolve(process.cwd(), 'src/lib/mermaid-client.ts'),
    'utf8'
  );
  assert.ok(
    mermaidSrc.includes('finalizeRenderedMermaidSvg'),
    'mermaid-client.ts must apply live copyright watermarks via finalizeRenderedMermaidSvg'
  );
  assert.ok(
    mermaidSrc.includes('enhanceMarkdownMermaidBlocks'),
    'mermaid-client.ts must wrap static Markdown Mermaid blocks in descriptive blueprint figures'
  );
  assert.ok(
    mermaidSrc.includes('bindDiagramExpand'),
    'mermaid-client.ts must bind fullscreen lightbox expansion controls'
  );
  assert.ok(
    mermaidSrc.includes('mermaid-blueprint-title'),
    'mermaid-client.ts must render plain descriptive .mermaid-blueprint-title headers'
  );
  assert.ok(
    mermaidSrc.includes('includeBackground: true'),
    'mermaid-client.ts must embed active theme surface background in standalone SVG/PNG exports'
  );

  const archSrc = fs.readFileSync(
    path.resolve(process.cwd(), 'src/components/ArchitectureView.astro'),
    'utf8'
  );
  assert.ok(
    archSrc.includes('finalizeRenderedMermaidSvg') && archSrc.includes('syncDiagramCardTitle'),
    'ArchitectureView.astro must sync descriptive titles and live watermarks'
  );
  assert.ok(
    archSrc.includes('data-expand-toggle="true"'),
    'ArchitectureView.astro must expose fullscreen lightbox toggle'
  );

  const pipelineSrc = fs.readFileSync(
    path.resolve(process.cwd(), 'src/components/PipelineView.astro'),
    'utf8'
  );
  assert.ok(
    pipelineSrc.includes('%% title:') &&
      pipelineSrc.includes('finalizeRenderedMermaidSvg') &&
      pipelineSrc.includes('syncDiagramCardTitle'),
    'PipelineView.astro must emit %% title directives, sync titles, and watermark SVGs'
  );
  assert.ok(
    pipelineSrc.includes('data-expand-toggle="true"'),
    'PipelineView.astro must expose fullscreen lightbox toggle'
  );

  const crossTopoSrc = fs.readFileSync(
    path.resolve(process.cwd(), 'src/components/CrossRepoTopology.astro'),
    'utf8'
  );
  assert.ok(
    crossTopoSrc.includes('%% title:') &&
      crossTopoSrc.includes('finalizeRenderedMermaidSvg') &&
      crossTopoSrc.includes('MutationObserver'),
    'CrossRepoTopology.astro must emit %% title, watermark SVGs, and re-render on theme toggle'
  );

  const cssSrc = fs.readFileSync(
    path.resolve(process.cwd(), 'src/styles/material-theme.css'),
    'utf8'
  );
  assert.ok(
    cssSrc.includes('.mermaid-blueprint-title') &&
      cssSrc.includes('.mermaid-lightbox-backdrop') &&
      cssSrc.includes('.m3-mermaid-host'),
    'material-theme.css must define Mermaid blueprint title, lightbox, and managed host rules'
  );
}

testSlugAndBasePathFormatting();
testM3ComponentsAndTokensPresent();
testUiLayoutAndDiagramTraversalContracts();
testHorizon2UiComponentsAndContracts();
testMermaidWatermarkAndTitleContracts();
console.log('AtlasSummary & Horizon 2 UI layout/diagram traversal checks passed.');
