"""Actual Chromium execution with deterministic local asset routes; public HTTPS not covered."""
from pathlib import Path
import json,re
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
assets={'./data/'+f:json.loads((R/'data'/f).read_text()) for f in ['architecture.json','content-manifest.json','explore.json','atlas.json','search/catalog.json','search/shard-map.json']}
for folder in ('packs','search/shards'):
 for f in (R/'data'/folder).glob('*.json'):assets['./data/'+folder+'/'+f.name]=json.loads(f.read_text())
html=re.sub(r'<script type="module"[^>]+></script>','',re.sub(r'<link rel="stylesheet"[^>]+>','',(R/'index.html').read_text()))
js='\n'.join([(R/'exploration.js').read_text().replace('export ',''),(R/'content-platform.js').read_text().replace('export ','').replace("import {rankSearch} from './exploration.js';",''),(R/'reader-window.js').read_text().replace('export ',''),(R/'app.js').read_text().replace("import {rankSearch,collectionFor} from './exploration.js';",'').replace("import {createPackLoader,createShardedSearch} from './content-platform.js';",'').replace("import {createReaderWindow} from './reader-window.js';",'')])
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 for width,height in [(1440,900),(390,844),(320,720)]:
  page=b.new_page(viewport={'width':width,'height':height});errors=[]
  page.on('pageerror',lambda err:errors.append(str(err)))
  page.set_content(html);page.add_style_tag(content=(R/'styles.css').read_text())
  page.evaluate('assets=>{window.assetLog=[];window.fetch=async p=>{window.assetLog.push(p);return {ok:!!assets[p],status:assets[p]?200:404,json:async()=>assets[p]}}}',assets)
  page.add_script_tag(content=js);page.wait_for_selector('.home-hero')
  assert page.locator('.chapter-collection-grid button').count()>=10
  page.evaluate('location.hash="#/chapter/V.1"');page.wait_for_selector('.chapter-complete')
  assert '10 available to read' in page.locator('.chapter-stats').inner_text()
  assert page.locator('.chapter-index .subchapter-btn').count()==10
  page.locator('.chapter-intro .btn-primary').click();page.wait_for_selector('.pathway-stop')
  assert page.locator('.pathway-stop').count()==10
  page.evaluate('location.hash="#/history/V.1.7"');page.wait_for_selector('.body-section')
  assert page.locator('.passage-evidence').count()>0
  page.locator('.passage-evidence summary').first.click()
  assert 'Academy of Korean Studies' in page.locator('.passage-evidence').first.inner_text()
  assert page.locator('.passage-evidence a').first.get_attribute('href').startswith('https://')
  page.keyboard.press('/');page.locator('#searchInput').fill('최승로')
  page.wait_for_function('document.querySelector(".search-results")?.textContent.includes("V.1.7")',timeout=16000)
  page.keyboard.press('Escape')
  page.evaluate('location.hash="#/timeline"');page.wait_for_selector('.timeline-page')
  assert 'Choe Seung-ro' in page.locator('body').inner_text()
  page.evaluate('location.hash="#/chapter/VII.5"');page.wait_for_selector('.chapter-complete')
  page.evaluate('location.hash="#/history/V.1.4"');page.wait_for_selector('.body-section')
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'overflow {width}'
  assert not errors,(width,errors)
  print(f'PASS Chromium {width}x{height}: Goryeo Chapter, complete route, source links, Korean search, chronology, legacy chapter, responsive layout')
  page.close()
 b.close()
