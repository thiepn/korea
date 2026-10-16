"""Chromium DOM acceptance of original app JavaScript with actual generated response payloads.

This is NOT HTTP-origin testing; no server or preview credentials are involved.
"""
from pathlib import Path
import re,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
assets={'./data/'+f:json.loads((ROOT/'data'/f).read_text()) for f in ['architecture.json','content-manifest.json','explore.json','atlas.json','search/catalog.json','search/shard-map.json']}
for folder in ('packs','search/shards'):
 for f in (ROOT/'data'/folder).glob('*.json'):
  assets['./data/'+folder+'/'+f.name]=json.loads(f.read_text())
html=re.sub(r'<script type="module"[^>]+></script>','',re.sub(r'<link rel="stylesheet"[^>]+>','',(ROOT/'index.html').read_text()) )
js='\n'.join([(ROOT/'exploration.js').read_text().replace('export ',''),(ROOT/'content-platform.js').read_text().replace('export ','').replace("import {rankSearch} from './exploration.js';",''),(ROOT/'reader-window.js').read_text().replace('export ',''),(ROOT/'app.js').read_text().replace("import {rankSearch,collectionFor} from './exploration.js';",'').replace("import {createPackLoader,createShardedSearch} from './content-platform.js';",'').replace("import {createReaderWindow} from './reader-window.js';",'')])
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 for w,h in [(1440,900),(390,844),(320,720)]:
  page=browser.new_page(viewport={'width':w,'height':h});errors=[]
  page.on('pageerror',lambda err:errors.append(str(err)))
  page.set_content(html);page.add_style_tag(content=(ROOT/'styles.css').read_text())
  page.evaluate('assets=>{window.assetLog=[];window.fetch=async p=>{window.assetLog.push(p);return {ok:!!assets[p],status:assets[p]?200:404,json:async()=>assets[p]}}}',assets)
  page.add_script_tag(content=js);page.wait_for_selector('.home-hero')
  assert page.locator('.chapter-collection-grid button').count()>=6
  page.evaluate('location.hash="#/chapter/IV.3"');page.wait_for_selector('.chapter-complete')
  assert '10 available to read' in page.locator('.chapter-stats').inner_text()
  assert page.locator('.chapter-index .subchapter-btn').count()==10
  page.locator('.chapter-intro .btn-primary').click();page.wait_for_selector('.pathway-stop')
  assert page.locator('.pathway-stop').count()==10
  page.evaluate('location.hash="#/history/IV.3.7"');page.wait_for_selector('.body-section')
  page.locator('[data-action=load-more]').first.click()
  page.wait_for_selector('.passage-evidence')
  assert page.locator('.passage-evidence').count()>=1
  page.locator('.passage-evidence summary').first.click()
  assert 'National Institute of Korean History' in page.locator('.passage-evidence').first.inner_text()
  assert page.locator('.passage-evidence a').first.get_attribute('href').startswith('https://')
  page.keyboard.press('/');page.locator('#searchInput').fill('장보고')
  page.wait_for_function('document.querySelector(".search-results")?.textContent.includes("IV.3.7")',timeout=12000)
  page.keyboard.press('Escape')
  page.evaluate('location.hash="#/timeline"');page.wait_for_selector('.timeline-page')
  assert 'Cheonghaejin' in page.locator('body').inner_text()
  page.evaluate('location.hash="#/chapter/III.2"');page.wait_for_selector('.chapter-complete')
  page.evaluate('location.hash="#/history/IV.3.2"');page.wait_for_selector('.body-section')
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'overflow at {w}'
  assert not errors,(w,errors)
  print(f'PASS Batch J Chromium {w}x{h}: sixth Chapter, ten-stop route, Korean search, evidence, atlas, previous Chapter, no overflow')
  page.close()
 browser.close()
