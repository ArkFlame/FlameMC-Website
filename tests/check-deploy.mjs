import assert from 'node:assert/strict';
import { readFileSync, existsSync, statSync } from 'node:fs';
import { resolve, join } from 'node:path';

// Reject a successful CI run that accidentally publishes the repository README.
const dist = resolve('dist');
const read = (file) => readFileSync(join(dist, file), 'utf8');
const present = (file) => assert.ok(existsSync(join(dist, file)), `Missing dist/${file}`);

const required = [
  'index.html', '404.html', 'CNAME', '.nojekyll', 'robots.txt',
  'favicon.svg', 'og-image.png', 'sitemap.xml', 'rss.xml',
  'styles/site.css', 'styles/content.css', 'scripts/site.js',
  'assets/chunk-network.webp', 'guides/index.html', 'download/index.html',
  'guides/paper-vs-folia/index.html',
  'guides/flamemc-vs-folia/index.html',
  'guides/canvas-vs-folia-vs-flamemc/index.html',
  'guides/folia-plugin-compatibility/index.html',
  'guides/minecraft-server-software-comparison-2026/index.html',
  'guides/region-threading-explained/index.html',
  'guides/universespigot-vs-flamemc/index.html',
];
for (const file of required) present(file);

const homepage = read('index.html');
assert.match(homepage, /<!doctype html>/i, 'Home must be generated HTML');
assert.match(homepage, /<h1\b/i, 'Missing hero heading');
assert.match(homepage, /Scale your world\./, 'Wrong page was built');
assert.match(homepage, /Keep your plugins\./, 'Wrong page was built');
assert.ok(!homepage.includes('Astro outputs `dist/`'), 'README was deployed instead of Astro');
assert.match(homepage, /https:\/\/builtbybit\.com\/resources\/flamemc-extreme-async-performance\.133143\//);
assert.equal(read('CNAME').trim(), 'flamemc.arkflame.com');
assert.match(read('sitemap.xml'), /<loc>https:\/\/flamemc\.arkflame\.com\/guides\/paper-vs-folia\/<\/loc>/);
assert.ok(statSync(join(dist, 'assets/chunk-network.webp')).size > 10000, 'Hero artwork missing or empty');
console.log(`PASS: verified ${required.length} GitHub Pages files, real Astro homepage, domain, sitemap and download link`);
