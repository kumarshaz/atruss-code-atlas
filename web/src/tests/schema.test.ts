import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const REQUIRED_DISCOVERY_FIELDS = [
  'Organization',
  'RepositoryName',
  'PrimaryLanguage',
  'FrameworkType',
  'DocumentationPriority',
  'HasDockerfile',
  'HasPipeline',
  'HasKubernetes',
  'HasAPI',
  'TechnologyStack',
];

function testExportsLatestContracts() {
  const reposJsonPath = path.resolve(process.cwd(), '../exports/latest/repos/repositories.json');
  assert.ok(fs.existsSync(reposJsonPath), `Missing discovery manifest: ${reposJsonPath}`);

  const payload = JSON.parse(fs.readFileSync(reposJsonPath, 'utf8'));
  const items = Array.isArray(payload) ? payload : payload.items;
  assert.ok(Array.isArray(items) && items.length > 0, 'repositories.json must contain items');

  for (const [idx, item] of items.entries()) {
    for (const key of REQUIRED_DISCOVERY_FIELDS) {
      assert.ok(
        Object.prototype.hasOwnProperty.call(item, key),
        `repositories.json item[${idx}] missing ${key}`
      );
    }
  }

  const astroConfigPath = path.resolve(process.cwd(), 'astro.config.mjs');
  const astroCfg = fs.readFileSync(astroConfigPath, 'utf8');
  assert.ok(astroCfg.includes('ASTRO_BASE'), 'astro.config.mjs must read ASTRO_BASE');
  assert.ok(astroCfg.includes('ASTRO_SITE'), 'astro.config.mjs must read ASTRO_SITE');
  assert.ok(
    !astroCfg.includes('github.com/organization/atruss-code-atlas'),
    'astro.config.mjs must not use placeholder organization URL'
  );
  assert.ok(
    astroCfg.includes('https://atruss.shashinkumar.com'),
    'astro.config.mjs must default site to https://atruss.shashinkumar.com'
  );
  assert.ok(
    !astroCfg.includes("'/atruss-code-atlas'") && !astroCfg.includes('"/atruss-code-atlas"'),
    'astro.config.mjs must not hardcode /atruss-code-atlas base path'
  );
}

function testHorizon2OptionalExportSchemas() {
  const latestDir = path.resolve(process.cwd(), '../exports/latest');

  const sbomDir = path.join(latestDir, 'sbom');
  if (fs.existsSync(sbomDir)) {
    const sbomFiles = fs.readdirSync(sbomDir).filter((f) => f.endsWith('.cdx.json'));
    for (const file of sbomFiles) {
      const sbom = JSON.parse(fs.readFileSync(path.join(sbomDir, file), 'utf8'));
      assert.equal(sbom.bomFormat, 'CycloneDX', `${file} must have bomFormat=CycloneDX`);
      assert.equal(sbom.specVersion, '1.6', `${file} must have specVersion=1.6`);
    }
  }

  const sarifDir = path.join(latestDir, 'sarif');
  if (fs.existsSync(sarifDir)) {
    const sarifFiles = fs.readdirSync(sarifDir).filter((f) => f.endsWith('.sarif.json'));
    for (const file of sarifFiles) {
      const sarif = JSON.parse(fs.readFileSync(path.join(sarifDir, file), 'utf8'));
      assert.equal(sarif.version, '2.1.0', `${file} must have SARIF version=2.1.0`);
      assert.ok(Array.isArray(sarif.runs), `${file} must contain runs array`);
    }
  }

  const historyPath = path.join(latestDir, 'catalog-history.json');
  if (fs.existsSync(historyPath)) {
    const history = JSON.parse(fs.readFileSync(historyPath, 'utf8'));
    assert.ok(Array.isArray(history.snapshots), 'catalog-history.json must contain snapshots array');
  }

  const llmsDir = path.join(latestDir, 'llms');
  if (fs.existsSync(llmsDir)) {
    const llmsTxt = path.join(llmsDir, 'llms.txt');
    const llmsFullTxt = path.join(llmsDir, 'llms-full.txt');
    if (fs.existsSync(llmsTxt)) {
      assert.ok(fs.readFileSync(llmsTxt, 'utf8').trim().length > 0, 'llms.txt must be non-empty');
    }
    if (fs.existsSync(llmsFullTxt)) {
      assert.ok(fs.readFileSync(llmsFullTxt, 'utf8').trim().length > 0, 'llms-full.txt must be non-empty');
    }
  }
}

testExportsLatestContracts();
testHorizon2OptionalExportSchemas();
console.log('Astro data contract & Horizon 2 schema checks passed.');
