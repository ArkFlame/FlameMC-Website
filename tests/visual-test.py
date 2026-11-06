import asyncio,json,re,base64
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
html=(ROOT/'src/pages/index.astro').read_text()
css=(ROOT/'public/styles/site.css').read_text()
js=(ROOT/'public/scripts/site.js').read_text()
html=html.replace('<link rel="stylesheet" href="/styles/site.css" />','<style>'+css+'</style>')
html=html.replace('<script is:inline src="/scripts/site.js" defer></script>','').replace('</body>','<script>'+js+'</script></body>')
for f in (ROOT/'public/assets').iterdir():
 if f.suffix=='.webp':
  html=html.replace('/assets/'+f.name, 'data:image/webp;base64,'+base64.b64encode(f.read_bytes()).decode('ascii'))

async def main():
 result={}
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
  for width,height in [(1440,900),(900,900),(390,844),(320,800)]:
   page=await browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1,reduced_motion='reduce' if width==320 else 'no-preference')
   errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   await page.set_content(html,wait_until='load')
   await page.evaluate('''async()=>{for(let y=0;y<document.documentElement.scrollHeight;y+=500){window.scrollTo({top:y,behavior:"instant"});await new Promise(r=>setTimeout(r,22));}window.scrollTo({top:0,behavior:"instant"})}''')
   await page.wait_for_timeout(1000)
   result[width]={
     'status':'inline preview',
     'title':await page.title(),
     'horizontalOverflow':await page.evaluate('document.documentElement.scrollWidth > window.innerWidth'),
     'bodyScrollWidth':await page.evaluate('document.body.scrollWidth'),
     'pageHeight':await page.evaluate('document.documentElement.scrollHeight'),
     'images':await page.locator('img').count(),
     'brokenImages':await page.evaluate('Array.from(document.images).filter(x=>!x.complete||!x.naturalWidth).map(x=>x.getAttribute("alt"))'),
     'missingReveal':await page.locator('[data-reveal]:not(.is-visible)').count(),
     'jsErrors':errors,
     'overflowElements':await page.evaluate('Array.from(document.querySelectorAll("body *")).filter(e=>e.getBoundingClientRect().right>innerWidth+1).slice(0,8).map(e=>({tag:e.tagName,cls:e.className?.baseVal||e.className,right:Math.round(e.getBoundingClientRect().right)}))')
   }
   if width==390:
    await page.locator('[data-menu-toggle]').click()
    result[width]['menuExpanded']=await page.locator('[data-menu-toggle]').get_attribute('aria-expanded')
    await page.keyboard.press('Escape')
    result[width]['menuClosedOnEscape']=await page.locator('[data-menu-toggle]').get_attribute('aria-expanded')
   target=ROOT/'previews'/f'home_{width}.png'
   await page.screenshot(path=str(target),full_page=True,animations='disabled')
   await page.close()
  await browser.close()
 print(json.dumps(result,indent=2))
 (ROOT/'previews'/'qa.json').write_text(json.dumps(result,indent=2))
asyncio.run(main())
