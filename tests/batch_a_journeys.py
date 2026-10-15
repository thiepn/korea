"""Focused real-DOM journeys using injected same-page assets; browser-origin acceptance remains separate."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,re
R=Path(__file__).resolve().parents[1]
A={'./data/'+p+'.json':json.loads((R/'data'/f'{p}.json').read_text()) for p in ('architecture','content-manifest','explore','search-index')}
for f in (R/'data/blocks').glob('*.json'):
 A['./data/blocks/'+f.name]=json.loads(f.read_text())
html=re.sub(r'<script type="module"[^>]+></script>','',re.sub(r'<link rel="stylesheet"[^>]+>','',(R/'index.html').read_text()))
js=(R/'exploration.js').read_text().replace('export ','')+'\n'+(R/'app.js').read_text().replace("import {rankSearch,collectionFor} from './exploration.js';",'')
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 for width,height in [(1440,900),(390,844)]:
  page=b.new_page(viewport={'width':width,'height':height})
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(html);page.add_style_tag(content=(R/'styles.css').read_text())
  page.evaluate('a=>{window.__assets=a;window.fetch=async path=>({ok:!!a[path],status:a[path]?200:404,json:async()=>a[path]})}',A)
  page.add_script_tag(content=js);page.wait_for_selector('.home-hero')
  # Themed discovery actually navigates through the first readable topic
  page.evaluate('location.hash="#/collection/everyday-worlds"');page.wait_for_selector('.pathway-stops')
  page.locator('[data-action=start-trail]').click();page.wait_for_selector('.body-section')
  assert page.evaluate('location.hash')=='#/history/I.1.4'
  # Search full text, filter, and open an exact canonical topic
  page.keyboard.press('/');page.locator('#searchInput').fill('tidal flat');page.wait_for_selector('.search-results button')
  assert 'I.1.4' in page.locator('.search-results button').first.inner_text()
  page.keyboard.press('Escape')
  # Reader detours save the anchor; staged restoration returns through planned topics
  page.locator('[data-action=load-more]').click();page.wait_for_function('document.querySelectorAll(".body-section").length===2')
  page.locator('[data-action=detour]').first.click();page.wait_for_selector('.reader-title')
  assert page.locator('[data-action=return-detour]').count()>0
  page.locator('[data-action=return-detour]').first.click();page.wait_for_selector('.body-section')
  page.wait_for_function('document.querySelectorAll(".body-section").length>=2')
  # Switch to endless, then cross a real passage boundary to next article
  page.locator('[data-action=mode][data-mode="endless"]').click();page.wait_for_selector('.body-section')
  for _ in range(7):
   buttons=page.locator('[data-action=load-more]')
   if buttons.count(): buttons.first.click()
   if page.locator('.segment-transition').count()>0:break
  assert page.locator('.segment-transition').count()>0,'endless failed to transition'
  assert page.locator('.body-section').count()>4,'endless did not fetch next article segment'
  # Bookmark and return to the library
  page.locator('[data-action=bookmark]').click()
  page.evaluate('location.hash="#/saved"');page.wait_for_selector('.saved-page')
  assert page.locator('.saved-row').count()>=1
  assert not errors,(width,errors)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
  print(f'PASS {width}x{height}: collection trail, corpus search, detour return, endless transition, local bookmark')
  page.close()
 b.close()
