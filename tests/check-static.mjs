import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
const root = new URL('../', import.meta.url).pathname;
const read = p => fs.readFileSync(path.join(root,p),'utf8');
const files = dir => fs.readdirSync(path.join(root,dir)).filter(s=>s.endsWith('.md'));
const home = read('src/pages/index.astro');
const layout = read('src/layouts/BaseLayout.astro');
const css = read('public/styles/site.css')+read('public/styles/content.css');
const js = read('public/scripts/site.js');
const listing = 'https://builtbybit.com/resources/flamemc-extreme-async-performance.133143/';
const guides = files('src/content/guides');
assert.equal(guides.length,7,'Expected seven source-backed guides');
assert.ok(!home.includes('href="#start"'),'Outdated CTA');
for (const source of [home,layout,read('src/pages/download/index.astro'),read('src/pages/guides/index.astro'),read('src/pages/guides/[slug].astro')]) {
  assert.ok(source.includes(listing),'Missing product CTA');
}
for(const [id,file] of [['top',home],['content',home],['advantages',home],['architecture',home],['comparison',home],['compatibility',home],['faq',home],['guides',home],['start',home]]) {
  assert.ok(file.includes(`id="${id}"`),`Missing home anchor ${id}`);
}
for (const ref of [...home.matchAll(/href="#([\w-]+)"/g)].map(m=>m[1])) assert.ok(home.includes(`id="${ref}"`),`Bad anchor: ${ref}`);
for (const ref of [...[home,layout].flatMap(s=>[...s.matchAll(/(?:src|href)="(\/[^"#]+\.(?:svg|webp|css|js|png))"/g)])].map(m=>m[1])) {
  assert.ok(fs.existsSync(path.join(root,'public',ref.slice(1))),`Missing asset ${ref}`);
}
for (const filename of guides) {
  const slug = filename.replace(/\.md$/,'');
  const content=read(`src/content/guides/${filename}`);
  for(const field of ['title','description','publishedAt','category','takeaway','readingMinutes']) assert.ok(new RegExp(`^${field}:`, 'm').test(content),`${filename} missing ${field}`);
  assert.ok(content.includes('https://'),'Article has no original/official links');
  assert.ok(content.length>1700,`${filename} insufficient depth`);
  for (const match of content.matchAll(/\]\(\/guides\/([^/]+)\/\)/g)) assert.ok(guides.includes(match[1]+'.md'),`Broken cross-guide link ${slug} -> ${match[1]}`);
}
assert.ok(layout.includes('application/ld+json'),'Schema missing');
assert.ok(layout.includes('rel="canonical"'),'Canonical missing');
assert.ok(read('src/pages/sitemap.xml.ts').includes('getCollection(\'guides\')'),'Sitemap not dynamic');
assert.ok(read('src/pages/rss.xml.ts').includes('getCollection(\'guides\')'),'RSS not dynamic');
assert.ok(!fs.existsSync(path.join(root,'public/sitemap.xml')),'Old static sitemap masks generated endpoint');
assert.ok(home.includes('Conceptual scheduling illustration, not a measured benchmark'));
assert.ok(css.includes('prefers-reduced-motion') && js.includes('aria-expanded'));
assert.equal(read('public/CNAME').trim(),'flamemc.arkflame.com');
const workflow = read('.github/workflows/deploy.yml');
assert.ok(workflow.includes('path: ./dist'), 'Pages must deploy dist, not the source root');
assert.ok(workflow.includes('npm run check:deploy'), 'Built output must be verified before uploading');
assert.ok(fs.existsSync(path.join(root, 'public/.nojekyll')), 'Missing Pages .nojekyll marker');
assert.ok(read('astro.config.mjs').includes('https://flamemc.arkflame.com'));
console.log(`PASS: ${guides.length} guides, canonical/OG/schema, CTA links, static assets, cross-links, generated sitemap/RSS, accessibility and disclaimer`);
