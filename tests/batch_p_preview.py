"""Read-only acceptance on the actual Cloudflare Pages branch preview, not synthetic assets."""
import os
from playwright.sync_api import sync_playwright
URL=os.getenv('KOREA_PREVIEW_URL','https://feat-batch-p-paleolithic-mod.korea-eo3.pages.dev').rstrip('/')
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 for width,height in ((1440,900),(390,844),(320,720)):
  page=browser.new_page(viewport={'width':width,'height':height})
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  response=page.goto(URL,wait_until='domcontentloaded',timeout=45000)
  assert response is not None and response.ok,('preview document failed',width,response.status if response else None)
  page.wait_for_selector('.home-hero',timeout=30000)
  manifest=page.evaluate("""async () => {
    const result=await fetch('./data/content-manifest.json',{cache:'no-store'});
    if (!result.ok) throw new Error('manifest unavailable');
    return await result.json();
  }""")
  assert manifest['count']==198 and manifest['sampleWordCount']>=161656,('stale preview corpus',manifest.get('count'),manifest.get('sampleWordCount'))
  for chapter in ('I.2','X.2'):
   page.evaluate('id=>location.hash="#/chapter/"+id',chapter)
   page.wait_for_selector('.chapter-complete')
   assert '10 available to read' in page.locator('.chapter-stats').inner_text()
   assert page.locator('.chapter-index .subchapter-btn').count()==10
   page.locator('.chapter-intro .btn-primary').click()
   page.wait_for_selector('.pathway-stop')
   assert page.locator('.pathway-stop').count()==10
  page.evaluate('location.hash="#/history/I.2.3"')
  page.wait_for_selector('.passage-evidence',timeout=30000)
  page.locator('.passage-evidence summary').first.click()
  assert 'National Museum of Korea' in page.locator('.passage-evidence').first.inner_text()
  page.keyboard.press('/')
  page.locator('#searchInput').fill('전곡리')
  page.wait_for_function('document.querySelector(".search-results")?.textContent.includes("I.2.3")',timeout=20000)
  page.keyboard.press('Escape')
  page.evaluate('location.hash="#/history/X.2.10"')
  page.wait_for_function('document.body.textContent.includes("Recovery in a world of repeated interruptions")',timeout=20000)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),('overflow',width)
  assert not errors,('browser errors',width,errors)
  page.close()
 browser.close()
print('PASS Batch P real Cloudflare preview 1440/390/320px: 198 articles, both ten-subject Chapters and routes, sourced reading, Korean search, economy, no overflow/errors')
