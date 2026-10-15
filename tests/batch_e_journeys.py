"""Real Chromium DOM acceptance; in-memory asset service, not remote HTTPS acceptance."""
from pathlib import Path
import json,re
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
assets={}
for filename in ['architecture.json','content-manifest.json','explore.json','atlas.json','search/catalog.json','search/shard-map.json']:
 assets['./data/'+filename]=json.loads((ROOT/'data'/filename).read_text())
for subdir in ['packs','search/shards']:
 for item in (ROOT/'data'/subdir).glob('*.json'):
  assets['./data/'+subdir+'/'+item.name]=json.loads(item.read_text())
html=re.sub(r'<script type="module"[^>]+></script>','',re.sub(r'<link rel="stylesheet"[^>]+>','',(ROOT/'index.html').read_text()))
js='\n'.join([
 (ROOT/'exploration.js').read_text().replace('export ',''),
 (ROOT/'content-platform.js').read_text().replace('export ','').replace("import {rankSearch} from './exploration.js';",''),
 (ROOT/'reader-window.js').read_text().replace('export ',''),
 (ROOT/'app.js').read_text().replace("import {rankSearch,collectionFor} from './exploration.js';",'').replace("import {createPackLoader,createShardedSearch} from './content-platform.js';",'').replace("import {createReaderWindow} from './reader-window.js';",'')])
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 for width,height in [(1440,900),(390,844),(320,720)]:
  page=browser.new_page(viewport={'width':width,'height':height});errors=[]
  page.on('pageerror',lambda x:errors.append(str(x)))
  page.set_content(html);page.add_style_tag(content=(ROOT/'styles.css').read_text())
  page.evaluate('a=>{window.assetLog=[];window.fetch=async p=>{window.assetLog.push(p);return {ok:!!a[p],status:a[p]?200:404,json:async()=>a[p]}}}',assets)
  page.add_script_tag(content=js)
  page.wait_for_selector('.home-hero')
  assert page.locator('.longform-shelf .story-card').count()==3
  assert page.locator('.era-card').count()==10
  page.evaluate('location.hash="#/collection/longform-history"');page.wait_for_selector('.pathway-stop')
  assert page.locator('.pathway-stop').count()==6
  page.evaluate('location.hash="#/history/V.5.6"');page.wait_for_selector('.reader-hero')
  assert '2,614' in page.locator('.reader-meta').inner_text()
  assert page.locator('.editorial-sources a').count()==2
  assert page.locator('.reader-timeline-context').count()==1
  page.locator('.editorial-sources summary').click()
  assert 'UNESCO' in page.locator('.editorial-sources').inner_text()
  assert page.locator('.reader-timeline-context button').count()==1
  page.evaluate('location.hash="#/history/VI.4.3"');page.wait_for_selector('.reader-hero')
  assert '2,670' in page.locator('.reader-meta').inner_text()
  assert 'Institutional' in page.locator('.editorial-sources').text_content()
  page.keyboard.press('/')
  page.locator('#searchInput').fill('훈민정음 창제')
  page.wait_for_function('document.querySelector(".search-results")?.textContent.includes("VI.4.3")',timeout=7500)
  page.keyboard.press('Escape')
  page.evaluate('location.hash="#/history/IX.3.3"');page.wait_for_selector('.reader-hero')
  assert '2,012' in page.locator('.reader-meta').inner_text()
  assert page.locator('.reader-rail .connection-reason').count()>=1 if width>800 else page.locator('.mobile-connections button').count()>=1
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'overflow {width}'
  assert not errors,(width,errors)
  print(f'PASS E Chromium {width}x{height}: canonical long reads, 6 references, themed path, atlas return links, Korean fulltext search, no overflow')
  page.close()
 browser.close()
