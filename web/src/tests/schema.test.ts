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
}

testExportsLatestContracts();
console.log('Astro data contract & schema checks passed.');
