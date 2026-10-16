"""Actual Chromium UI exercise with deterministic local content; not public HTTPS testing."""
from pathlib import Path
import re,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
assets={'./data/'+f:json.loads((ROOT/'data'/f).read_text()) for f in ['architecture.json','content-manifest.json','explore.json','atlas.json','search/catalog.json','search/shard-map.json']}
for folder in ['packs','search/shards']:
 for f in (ROOT/'data'/folder).glob('*.json'):
  assets['./data/'+folder+'/'+f.name]=json.loads(f.read_text())
html=re.sub(r'<script type="module"[^>]+></script>','',re.sub(r'<link rel="stylesheet"[^>]+>','',(ROOT/'index.html').read_text()))
js='\n'.join([(ROOT/'exploration.js').read_text().replace('export ',''),(ROOT/'content-platform.js').read_text().replace('export ','').replace("import {rankSearch} from './exploration.js';",''),(ROOT/'reader-window.js').read_text().replace('export ',''),(ROOT/'app.js').read_text().replace("import {rankSearch,collectionFor} from './exploration.js';",'').replace("import {createPackLoader,createShardedSearch} from './content-platform.js';",'').replace("import {createReaderWindow} from './reader-window.js';",'')])
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 for w,h in [(1440,900),(390,844),(320,720)]:
  page=browser.new_page(viewport={'width':w,'height':h});errors=[]
  page.on('pageerror',lambda err:errors.append(str(err)))
  page.set_content(html);page.add_style_tag(content=(ROOT/'styles.css').read_text())
  page.evaluate('assets=>{window.assetLog=[];window.fetch=async p=>{window.assetLog.push(p);return {ok:!!assets[p],status:assets[p]?200:404,json:async()=>assets[p]}}}',assets)
  page.add_script_tag(content=js);page.wait_for_selector('.home-hero')
  assert page.locator('.chapter-collection-grid button').count()==3
  for chapter in ['III.3','VI.4','IX.3']:
   page.evaluate('chapter=>location.hash="#/chapter/"+chapter',chapter)
   page.wait_for_selector('.chapter-complete')
   assert '10 available to read' in page.locator('.chapter-stats').inner_text()
   assert page.locator('.chapter-index .subchapter-btn').count()==10
   page.locator('.chapter-intro .btn-primary').click()
   page.wait_for_selector('.pathway-stop')
   assert page.locator('.pathway-stop').count()==10
  page.evaluate('location.hash="#/history/III.3.3"');page.wait_for_selector('.body-section')
  assert page.locator('.passage-evidence').count()==1
  page.locator('.passage-evidence summary').click()
  assert 'Gwanggaeto' in page.locator('.passage-evidence').inner_text()
  page.keyboard.press('/');page.locator('#searchInput').fill('선덕여왕')
  page.wait_for_function('document.querySelector(".search-results")?.textContent.includes("III.3.9")',timeout=8000)
  page.keyboard.press('Escape')
  page.evaluate('location.hash="#/history/VI.4.5"');page.wait_for_selector('.body-section')
  assert page.locator('.passage-evidence').count()==1
  page.locator('.passage-evidence summary').click()
  assert 'National Hangeul Museum' in page.locator('.passage-evidence').inner_text()
  assert page.locator('.passage-evidence a').first.get_attribute('href').startswith('https://')
  page.evaluate('location.hash="#/history/IX.3.9"');page.wait_for_selector('.body-section')
  page.locator('[data-action="load-more"]').first.click()
  page.wait_for_function('document.querySelectorAll(".body-section").length>=2')
  page.locator('[data-action="load-more"]').first.click()
  page.wait_for_function('document.querySelectorAll(".body-section").length>=3')
  page.locator('.passage-evidence').last.locator('summary').click()
  assert 'repatriation' in page.locator('.passage-evidence').last.inner_text().lower()
  page.keyboard.press('/');page.locator('#searchInput').fill('포로 송환')
  page.wait_for_function('document.querySelector(".search-results")?.textContent.includes("IX.3.9")',timeout=8000)
  page.keyboard.press('Escape')
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'overflow at {w}'
  assert not errors,(w,errors)
  print(f'PASS G Chromium {w}x{h}: complete VI.4/IX.3 chapters, themed reading routes, passage evidence, Korean search, responsive layout')
  page.close()
 browser.close()
