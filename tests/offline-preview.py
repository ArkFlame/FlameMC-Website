"""Visual-only browser fixture assembled from Astro markup + Markdown.
NOT an Astro compiler and NOT production build verification.
"""
import html,json,re,shutil,yaml,os
from pathlib import Path
from markdown_it import MarkdownIt
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get('FLAMEMC_PREVIEW_OUTPUT',str(ROOT/'preview-fixture')))
OUT.mkdir(parents=True,exist_ok=True)
for item in ('assets','styles','scripts'):
 shutil.copytree(ROOT/'public'/item,OUT/item,dirs_exist_ok=True)
for item in ('favicon.svg','og-image.png'):
 shutil.copy2(ROOT/'public'/item,OUT/item)
layout=(ROOT/'src/layouts/BaseLayout.astro').read_text().split('---',2)[-1]
# Remove dynamic tag fragments and replace props with fixture data
layout=re.sub(r'\{publishedTime && <meta.*?/>\}', '', layout)
layout=re.sub(r'\{modifiedTime && <meta.*?/>\}', '', layout)
layout=re.sub(r'<script type="application/ld\+json" set:html=\{.*?\}></script>', '<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebSite","name":"FlameMC"}</script>', layout)

def make(body,title,description,url):
 out=layout
 out=out.replace('<slot />',body)
 out=out.replace('{title}',html.escape(title))
 out=out.replace('{description}',html.escape(description))
 out=out.replace('content={description}',f'content="{html.escape(description)}"')
 out=out.replace('href={canonical}',f'href="https://flamemc.arkflame.com{url}"')
 out=out.replace('content={canonical}',f'content="https://flamemc.arkflame.com{url}"')
 out=out.replace('content={imageUrl}','content="https://flamemc.arkflame.com/og-image.png"')
 out=out.replace('content={type}','content="website"')
 assert '<slot' not in out
 dest=OUT/url.lstrip('/')/'index.html' if url!='/' else OUT/'index.html'
 dest.parent.mkdir(parents=True,exist_ok=True)
 dest.write_text(out)
 return dest
home=(ROOT/'src/pages/index.astro').read_text()
main=home[home.index('  <main id="content">'):home.rindex('</main>')+7]
make(main,'FlameMC — Folia Multithreading with Paper Plugin Compatibility','Folia multithreading with supported Paper compatibility. FlameMC now available.','/')

# Markdown pages render with same CSS/design as Astro templates, without replacing Astro build.
posts={}
for path in sorted((ROOT/'src/content/guides').glob('*.md')):
 data,body=path.read_text().split('---',2)[1:]
 posts[path.stem]=(yaml.safe_load(data),body)

def esc(x):return html.escape(str(x),quote=True)
order=['minecraft-server-software-comparison-2026','paper-vs-folia','flamemc-vs-folia','canvas-vs-folia-vs-flamemc','folia-plugin-compatibility','region-threading-explained','universespigot-vs-flamemc']
cards=''
for i,slug in enumerate(order):
 data,_=posts[slug]
 cards+=f'''<a href="/guides/{slug}/" class="editorial-card {'editorial-card-featured' if i==0 else ''}"><div class="editorial-card-top"><span>{esc(data['category']).upper()}</span><span>{i+1:02d} / 07</span></div><h2>{esc(data['title'])}</h2><p>{esc(data['description'])}</p><div class="editorial-card-footer"><span>{data['readingMinutes']} MIN READ</span><span class="editorial-card-arrow">↗</span></div></a>'''
listing='https://builtbybit.com/resources/flamemc-extreme-async-performance.133143/'
cta=f'''<section class="container editorial-cta"><div><span class="kicker">THE FLAMEMC APPROACH</span><h2>The concurrency of Folia.<br/><span>The ecosystem of Paper.</span></h2><p>A server built for region threading and supported Paper workflows.</p></div><a class="button button-primary" href="{listing}" target="_blank">Get FlameMC ↗</a></section>'''
index_body=f'''<main id="content" class="editorial-page"><section class="editorial-hero container"><div class="editorial-overline"><span class="status-led"></span> FLAMEMC FIELD NOTES <span class="editorial-divider">/</span> ARCHITECTURE & GUIDES</div><h1>Understand the engine.<br/><span>Choose the right server.</span></h1><p class="editorial-lede">Source-backed explanations of Minecraft server threading, Paper plugin compatibility, and the trade-offs between today's server forks. Built for administrators and developers making real deployment decisions.</p><div class="editorial-meta">7 GUIDES <span>·</span> UPDATED NOVEMBER 2026 <span>·</span> NO INVENTED BENCHMARKS</div></section><section class="container editorial-feed">{cards}</section>{cta}</main>'''
make(index_body,'Minecraft Server Guides & Comparisons | FlameMC','Technical guides to Paper Folia Canvas FlameMC and UniverseSpigot','/guides/')
md=MarkdownIt('commonmark').enable('table')
for slug,(data,body) in posts.items():
 article=md.render(body)
 related=''.join(f'<a class="related-card" href="/guides/{other}/"><span>{esc(posts[other][0]["category"]).upper()}</span><h3>{esc(posts[other][0]["title"])}</h3><span class="related-arrow">↗</span></a>' for other in order if other!=slug)[:0] # populated below
 related=''.join(f'<a class="related-card" href="/guides/{other}/"><span>{esc(posts[other][0]["category"]).upper()}</span><h3>{esc(posts[other][0]["title"])}</h3><span class="related-arrow">↗</span></a>' for other in order if other!=slug) if False else ''.join(f'<a class="related-card" href="/guides/{other}/"><span>{esc(posts[other][0]["category"]).upper()}</span><h3>{esc(posts[other][0]["title"])}</h3><span class="related-arrow">↗</span></a>' for other in [x for x in order if x!=slug][:3])
 intro=f'''<main id="content" class="editorial-page article-page"><article class="container article-shell"><nav class="article-breadcrumb"><a href="/">FlameMC</a><span>/</span><a href="/guides/">Guides</a><span>/</span><span>{esc(data['category'])}</span></nav><header class="article-header"><div class="editorial-overline"><span class="status-led"></span> {esc(data['category']).upper()} <span class="editorial-divider">/</span> FLAMEMC FIELD NOTES</div><h1>{esc(data['title'])}</h1><p class="article-deck">{esc(data['description'])}</p><div class="article-byline"><span>FLAMEMC</span><span>·</span><span>NOVEMBER 5, 2026</span><span>·</span><span>{data['readingMinutes']} MIN READ</span></div></header><div class="article-layout"><aside class="article-aside"><span class="aside-label">THE SHORT ANSWER</span><p>{esc(data['takeaway'])}</p><div class="aside-rule"></div><a href="/guides/">ALL GUIDES ↗</a></aside><div class="article-content prose">{article}</div></div></article><section class="container related-section"><div class="related-heading"><span class="kicker">KEEP READING</span><h2>Related guides.</h2></div><div class="related-grid">{related}</div></section><section class="container article-bottom-cta"><div><span class="kicker">NOW AVAILABLE</span><h2>Scale your world.<br/><span>Keep your plugins.</span></h2><p>Explore FlameMC on BuiltByBit and check current release details.</p></div><a class="button button-primary" href="{listing}" target="_blank">Get FlameMC ↗</a></section></main>'''
 make(intro,data['title']+' | FlameMC',data['description'],f'/guides/{slug}/')
source=(ROOT/'src/pages/download/index.astro').read_text()
main=source[source.index('  <main id="content"'):source.rindex('</main>')+7]
main=main.replace('href={listing}',f'href="{listing}"')
make(main,'Download FlameMC — Available Now','Get FlameMC on BuiltByBit','/download/')
print('Static visual-fixture pages:',len(list(OUT.rglob('index.html'))),'at',OUT)
