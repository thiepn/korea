"""Batch AC exact Cloudflare Pages branch-preview real-origin Chromium acceptance."""
import json,os,time
from playwright.sync_api import sync_playwright
URL=os.environ['KOREA_PREVIEW_URL'].rstrip('/')
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
    for w,h in ((1440,900),(390,844),(320,720)):
        page=browser.new_page(viewport={'width':w,'height':h})
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        for attempt in range(15):
            response=page.goto(URL,wait_until='domcontentloaded',timeout=45000)
            assert response and response.ok,('Cloudflare preview document failed',w,response.status if response else None)
            page.wait_for_selector('.home-hero',timeout=20000)
            manifest=page.evaluate("""async()=>{const r=await fetch('./data/content-manifest.json',{cache:'no-store'});if(!r.ok)throw Error('missing manifest');return await r.json()}""")
            if manifest.get('count')>=423 and manifest.get('sampleWordCount',0)>=427740:break
            if attempt==14:raise AssertionError(('stale or incorrect deployed assets',manifest.get('count'),manifest.get('sampleWordCount')))
            time.sleep(5)
        for ch in ('I.5','IV.2'):
            page.evaluate('id=>location.hash="#/chapter/"+id',ch);page.wait_for_selector('.chapter-complete')
            assert '10 available to read' in page.locator('.chapter-stats').inner_text()
            assert page.locator('.chapter-index .subchapter-btn').count()==10
            page.locator('.chapter-intro .btn-primary').click();page.wait_for_selector('.pathway-stop')
            assert page.locator('.pathway-stop').count()==10
        page.evaluate('location.hash="#/history/I.5.2"');page.wait_for_selector('.passage-evidence',timeout=30000)
        page.locator('.passage-evidence summary').first.click()
        assert 'National Museum of Korea' in page.locator('.passage-evidence').first.inner_text()
        page.keyboard.press('/');page.locator('#searchInput').fill('신라 촌락문서')
        page.wait_for_function('document.querySelector(".search-results")?.textContent.includes("IV.2.7")',timeout=20000)
        page.keyboard.press('Escape')
        page.evaluate('location.hash="#/history/IV.2.10"')
        page.wait_for_function('document.body.textContent.includes("The capital was not simply a ceremonial backdrop")',timeout=20000)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),('horizontal overflow',w)
        assert not errors,(w,errors)
        page.close()
    browser.close()
print('PASS real-origin Cloudflare Preview: 423 articles, both Chapters, 1440/390/320px, source notes, Korean search and no overflow.')
