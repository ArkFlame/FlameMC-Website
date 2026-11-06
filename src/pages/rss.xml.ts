import { getCollection } from 'astro:content';
const site = 'https://flamemc.arkflame.com';
const escapeXml = (value: string) => value.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
export async function GET() {
  const guides = (await getCollection('guides')).sort((a,b)=>b.data.publishedAt.getTime()-a.data.publishedAt.getTime());
  const items = guides.map(g=>`<item><title>${escapeXml(g.data.title)}</title><link>${site}/guides/${g.id}/</link><guid isPermaLink="true">${site}/guides/${g.id}/</guid><description>${escapeXml(g.data.description)}</description><pubDate>${g.data.publishedAt.toUTCString()}</pubDate></item>`).join('');
  return new Response(`<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>FlameMC Guides</title><link>${site}/guides/</link><description>Minecraft server architecture, Folia threading and Paper plugin compatibility</description><language>en</language>${items}</channel></rss>`,{headers:{'Content-Type':'application/rss+xml; charset=utf-8'}});
}
