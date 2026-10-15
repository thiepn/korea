"""Browser implementation acceptance with a deterministic mocked network for compiled assets.
Not an HTTP-origin/certificate test. Tests real interactive app JS/CSS in Chromium.
"""
from pathlib import Path
import json,re
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent.parent
sources=['architecture.json','content-manifest.json','explore.json','search/catalog.json','search/shard-map.json']
ASSETS={'./data/'+p:json.loads((ROOT/'data'/p).read_text()) for p in sources}
for folder in ['packs','search/shards']:
 for file in (ROOT/'data'/folder).glob('*.json'):
  ASSETS['./data/'+folder+'/'+file.name]=json.loads(file.read_text())
html=re.sub(r'<script type="module"[^>]+></script>','',re.sub(r'<link rel="stylesheet"[^>]+>','',(ROOT/'index.html').read_text()))
js=(ROOT/'exploration.js').read_text().replace('export ','')+'\n'+(ROOT/'content-platform.js').read_text().replace('export ','').replace("import {rankSearch} from './exploration.js';",'')+'\n'+(ROOT/'reader-window.js').read_text().replace('export ','')+'\n'+(ROOT/'app.js').read_text().replace("import {rankSearch,collectionFor} from './exploration.js';",'').replace("import {createPackLoader,createShardedSearch} from './content-platform.js';",'').replace("import {createReaderWindow} from './reader-window.js';",'')
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 for w,h in [(1440,900),(390,844),(320,720)]:
  page=browser.new_page(viewport={'width':w,'height':h});errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(html);page.add_style_tag(content=(ROOT/'styles.css').read_text())
  page.evaluate('assets=>{window.__assets=assets;window.__fetchLog=[];window.fetch=async p=>{window.__fetchLog.push(p);return {ok:!!assets[p],status:assets[p]?200:404,json:async()=>assets[p]}}}',ASSETS)
  page.add_script_tag(content=js);page.wait_for_selector('.home-hero',timeout=7500)
  assert page.evaluate('window.__fetchLog.every(x=>!x.includes("shards"))'),'search shards loaded before search'
  assert page.locator('.era-card').count()==10
  page.evaluate('location.hash="#/part/VI"');page.wait_for_selector('.chapter-row');assert page.locator('.chapter-row').count()==10
  page.evaluate('location.hash="#/chapter/VI.4"');page.wait_for_selector('.subchapter-btn');assert page.locator('.subchapter-btn').count()==10
  page.evaluate('location.hash="#/history/VI.4.1"');page.wait_for_selector('.body-section')
  assert page.locator('.body-section').count()==1
  assert page.evaluate('window.__fetchLog.some(x=>x.includes("/packs/"))'),'pack fetch missing'
  page.locator('[data-action=load-more]').click();page.wait_for_function('document.querySelectorAll(".body-section").length>=2')
  page.locator('[data-action=bookmark]').click()
  page.keyboard.press('/');page.locator('#searchInput').fill('river terraces')
  page.wait_for_function('document.querySelector(".search-results")?.textContent.includes("I.2.1")',timeout=7000)
  page.wait_for_function('window.__fetchLog.some(x=>x.includes("search/shards"))',timeout=7500)
  page.locator('[data-filter="planned"]').click();page.wait_for_timeout(200)
  assert page.locator('.search-results button').count()==0
  page.keyboard.press('Escape')
  page.locator('[data-action=mode][data-mode="overview"]').click();page.wait_for_selector('.overview-topics')
  assert page.locator('.overview-link').count()==4
  page.locator('.mode-tabs [data-action=mode][data-mode="endless"]').click();page.wait_for_selector('.body-section')
  for i in range(13):
   btn=page.locator('[data-action=load-more]')
   if btn.count()==0:break
   btn.first.click(timeout=7000)
   page.wait_for_timeout(30)
  assert page.locator('.body-section').count()>=4
  page.evaluate('location.hash="#/saved"');page.wait_for_selector('.saved-page');assert page.locator('.saved-row').count()>=1
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'horizontal overflow at {w}'
  assert not errors,(w,errors)
  print(f'PASS {w}x{h}: original 10/100 navigation, V1 reading continuity, bounded packs, lazy full-text shards, local bookmarks, modes, responsive layout')
  page.close()
 browser.close()
