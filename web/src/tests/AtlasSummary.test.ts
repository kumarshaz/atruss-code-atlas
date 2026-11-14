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
}

testSlugAndBasePathFormatting();
testM3ComponentsAndTokensPresent();
testUiLayoutAndDiagramTraversalContracts();
console.log('AtlasSummary & UI layout/diagram traversal checks passed.');
