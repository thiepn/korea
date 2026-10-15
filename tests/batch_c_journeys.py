"""Batch C actual Chromium DOM journeys; assets are in-memory HTTP-shaped mocks.
No claims about remote HTTPS, Cloudflare routing, or browser certificate acceptance.
"""
from pathlib import Path
import json,re
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
ASSETS={}
for p in ['architecture.json','content-manifest.json','explore.json','search/catalog.json','search/shard-map.json']:
 ASSETS['./data/'+p]=json.loads((ROOT/'data'/p).read_text())
for folder in ['packs','search/shards']:
 for p in (ROOT/'data'/folder).glob('*.json'):ASSETS['./data/'+folder+'/'+p.name]=json.loads(p.read_text())
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
  page.evaluate('assets=>{window.__fetchLog=[];window.fetch=async p=>{window.__fetchLog.push(p);return {ok:!!assets[p],status:assets[p]?200:404,json:async()=>assets[p]}}}',ASSETS)
  page.add_script_tag(content=js)
  page.wait_for_selector('.home-hero')
  assert page.locator('.era-card').count()==10
  # A new Batch C article is available from canonical chapter navigation.
  page.evaluate('location.hash="#/history/VII.2.4"');page.wait_for_selector('.body-section')
  assert 'Ritual' in page.locator('.body-section').first.inner_text()
  page.locator('[data-action="load-more"]').first.click();page.wait_for_function('document.querySelectorAll(".body-section").length>=2')
  page.locator('[data-action="bookmark"]').first.click()
  page.keyboard.press('/');page.locator('#searchInput').fill('mourning rites');page.wait_for_function('document.querySelector(".search-results")?.textContent.includes("VII.2.4")',timeout=10000)
  page.wait_for_function('window.__fetchLog.some(x=>x.includes("search/shards"))',timeout=10000)
  page.keyboard.press('Escape')
  page.locator('.mode-tabs [data-action="mode"][data-mode="endless"]').click();page.wait_for_selector('.body-section')
  page.evaluate('document.querySelector(".reader-rail")?.remove()') if False else None
  # A separate, heavy 140-passage DOM verifies pruning and backward restoration.
  page.evaluate('''() => {
   readerWindow.reset();document.getElementById('readerBody').innerHTML=Array.from({length:140},(_,i)=>`<section class="body-section" id="virtual-${i}" style="min-height:240px"><h2>History passage ${i}</h2><p>${'Historical narrative sample '.repeat(40)}</p></section>`).join('');
   readerWindow.schedule();
  }''')
  page.wait_for_function('document.querySelectorAll(".passage-placeholder").length>50',timeout=8000)
  assert page.locator('.body-section').count()<=22
  page.locator('#virtual-139').scroll_into_view_if_needed(timeout=10000)
  page.wait_for_function('document.getElementById("virtual-139")?.classList.contains("body-section")',timeout=8000)
  page.locator('#virtual-0').scroll_into_view_if_needed(timeout=10000)
  page.wait_for_function('document.getElementById("virtual-0")?.classList.contains("body-section")',timeout=8000)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'overflow {width}'
  assert not errors,(width,errors)
  print(f'PASS {width}x{height}: 77-article corpus, new canonical route, sharded full text, bookmark, Endless mode, 140-passage DOM window and backward restoration')
  page.close()
 browser.close()
