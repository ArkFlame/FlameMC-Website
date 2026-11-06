import { getCollection } from 'astro:content';
const site = 'https://flamemc.arkflame.com';
const escapeXml = (value: string) => value.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
export async function GET() {
  const guides = await getCollection('guides');
  const urls = [
    { path: '/', priority: 1, modified: '2026-11-05' },
    { path: '/download/', priority: .9, modified: '2026-11-05' },
    { path: '/guides/', priority: .9, modified: '2026-11-05' },
    ...guides.map(guide=>({path:`/guides/${guide.id}/`, priority:.8, modified:(guide.data.updatedAt ?? guide.data.publishedAt).toISOString().slice(0,10)})),
  ];
  const body = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls.map(item=>`  <url><loc>${escapeXml(site+item.path)}</loc><lastmod>${item.modified}</lastmod><priority>${item.priority.toFixed(1)}</priority></url>`).join('\n') + '\n</urlset>';
  return new Response(body,{headers:{'Content-Type':'application/xml; charset=utf-8'}});
}
