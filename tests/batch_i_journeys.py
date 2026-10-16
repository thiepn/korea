"""Real Chromium JS/DOM acceptance via deterministic local asset responses."""
from pathlib import Path
import re,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
assets={'./data/'+f:json.loads((R/'data'/f).read_text()) for f in ['architecture.json','content-manifest.json','explore.json','atlas.json','search/catalog.json','search/shard-map.json']}
for folder in ['packs','search/shards']:
 for f in (R/'data'/folder).glob('*.json'):assets['./data/'+folder+'/'+f.name]=json.loads(f.read_text())
html=re.sub(r'<script type="module"[^>]+></script>','',re.sub(r'<link rel="stylesheet"[^>]+>','',(R/'index.html').read_text()))
js='\n'.join([(R/'exploration.js').read_text().replace('export ',''),(R/'content-platform.js').read_text().replace('export ','').replace("import {rankSearch} from './exploration.js';",''),(R/'reader-window.js').read_text().replace('export ',''),(R/'app.js').read_text().replace("import {rankSearch,collectionFor} from './exploration.js';",'').replace("import {createPackLoader,createShardedSearch} from './content-platform.js';",'').replace("import {createReaderWindow} from './reader-window.js';",'')])
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 for w,h in [(1440,900),(390,844),(320,720)]:
  page=browser.new_page(viewport={'width':w,'height':h});errs=[];page.on('pageerror',lambda e:errs.append(str(e)))
  page.set_content(html);page.add_style_tag(content=(R/'styles.css').read_text())
  page.evaluate('assets=>{window.assetLog=[];window.fetch=async p=>{window.assetLog.push(p);return {ok:!!assets[p],status:assets[p]?200:404,json:async()=>assets[p]}}}',assets)
  page.add_script_tag(content=js);page.wait_for_selector('.home-hero')
  assert page.locator('.chapter-collection-grid button').count()>=5
  page.evaluate('location.hash="#/chapter/III.2"');page.wait_for_selector('.chapter-complete')
  assert '10 available to read' in page.locator('.chapter-stats').inner_text()
  assert page.locator('.chapter-index .subchapter-btn').count()==10
  page.locator('.chapter-intro .btn-primary').click();page.wait_for_selector('.pathway-stop')
  assert page.locator('.pathway-stop').count()==10
  page.evaluate('location.hash="#/history/III.2.8"');page.wait_for_selector('.body-section')
  assert page.locator('.passage-evidence').count()>=1
  page.locator('.passage-evidence summary').first.click()
  assert 'Cultural Heritage' in page.locator('.passage-evidence').first.inner_text()
  assert page.locator('.passage-evidence a').first.get_attribute('href').startswith('https://')
  page.keyboard.press('/');page.locator('#searchInput').fill('무령왕릉')
  page.wait_for_function('document.querySelector(".search-results")?.textContent.includes("III.2.8")',timeout=12000)
  page.keyboard.press('Escape')
  page.evaluate('location.hash="#/timeline"');page.wait_for_selector('.timeline-page')
  assert 'King Muryeong' in page.locator('body').inner_text()
  page.evaluate('location.hash="#/chapter/VI.4"');page.wait_for_selector('.chapter-complete')
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'overflow at {w}'
  assert not errs,(w,errs)
  print(f'PASS Batch I Chromium {w}x{h}: fifth complete Chapter, ten-stop pathway, evidence, Korean search, timeline, earlier Chapters, no overflow')
  page.close()
 browser.close()
