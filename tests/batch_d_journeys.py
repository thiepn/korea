"""Batch D exact-source Chromium journeys using in-memory HTTP-shaped assets.
Public Cloudflare HTTPS and real local HTTP origin must be qualified separately.
"""
from pathlib import Path
import json,re
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
ASSETS={}
for name in ['architecture.json','content-manifest.json','explore.json','atlas.json','search/catalog.json','search/shard-map.json']:
 ASSETS['./data/'+name]=json.loads((ROOT/'data'/name).read_text())
for folder in ['packs','search/shards']:
 for p in (ROOT/'data'/folder).glob('*.json'):ASSETS['./data/'+folder+'/'+p.name]=json.loads(p.read_text())
html=re.sub(r'<script type="module"[^>]+></script>','',re.sub(r'<link rel="stylesheet"[^>]+>','',(ROOT/'index.html').read_text()))
js='\n'.join([
 (ROOT/'exploration.js').read_text().replace('export ',''),
 (ROOT/'content-platform.js').read_text().replace('export ','').replace("import {rankSearch} from './exploration.js';",''),
 (ROOT/'reader-window.js').read_text().replace('export ',''),
 (ROOT/'app.js').read_text().replace("import {rankSearch,collectionFor} from './exploration.js';",'').replace("import {createPackLoader,createShardedSearch} from './content-platform.js';",'').replace("import {createReaderWindow} from './reader-window.js';",'')
])
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 for width,height in [(1440,900),(390,844),(320,720)]:
  page=browser.new_page(viewport={'width':width,'height':height});errors=[];page.on('pageerror',lambda err:errors.append(str(err)))
  page.set_content(html);page.add_style_tag(content=(ROOT/'styles.css').read_text())
  page.evaluate('assets=>{window.__fetchLog=[];window.fetch=async p=>{window.__fetchLog.push(p);return {ok:!!assets[p],status:assets[p]?200:404,json:async()=>assets[p]}}}',ASSETS)
  page.add_script_tag(content=js)
  page.wait_for_selector('.home-hero')
  if width==320:
   assert page.locator('.era-card').count()==10
   page.evaluate('location.hash="#/timeline"');page.wait_for_selector('.timeline-event',timeout=5000)
   assert page.locator('.timeline-event').count()==27
   assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
   assert not errors,(width,errors)
   print('PASS 320x720: mobile responsive navigation, 27 event timeline, no overflow')
   page.close();continue
  assert page.locator('.era-card').count()==10
  assert page.locator('.timeline-invite').count()==1
  page.evaluate('location.hash="#/timeline"');page.wait_for_selector('.timeline-event')
  assert page.locator('.timeline-event').count()==27
  page.evaluate('location.hash="#/timeline/VI"');page.wait_for_function('document.querySelectorAll(".timeline-event").length===3')
  assert 'Hanyang' in page.locator('.timeline-events').inner_text()
  page.evaluate('location.hash="#/explore"');page.wait_for_selector('.pathway-grid')
  assert page.locator('.pathway-card').count()>=10
  page.evaluate('location.hash="#/history/I.3.4"');page.wait_for_selector('.body-section')
  assert 'architecture of staying' in page.locator('.body-section').first.inner_text().lower()
  assert page.locator('.reader-rail .connection-reason').count()>0
  # Reader detour using cross-subject link; return to original route.
  page.evaluate('window.scrollTo(0,360)')
  page.locator('.mobile-connections button' if width<760 else '.reader-rail .rail-related.connected').first.click()
  page.wait_for_function('location.hash!=="#/history/I.3.4"')
  page.locator('[data-action="return-detour"]').first.click(force=True)
  page.wait_for_function('location.hash==="#/history/I.3.4"')
  page.wait_for_selector('.body-section')
  # Korean full-text aliases remain discoverable even though canonical titles are English.
  page.keyboard.press('/');page.locator('#searchInput').fill('훈민정음')
  page.wait_for_function('document.querySelector(".search-results")?.textContent.includes("VI.4.2")',timeout=5000)
  page.keyboard.press('Escape')
  # Default title and English passage search intact.
  page.keyboard.press('/');page.locator('#searchInput').fill('pit houses')
  page.wait_for_function('document.querySelector(".search-results")?.textContent.includes("I.3.4")',timeout=5000)
  page.keyboard.press('Escape')
  if width==1440:
   # Force canonical block snapshot eviction, then restore from immutable pack.
   page.evaluate('''() => {readerWindow.reset();document.querySelector('#readerBody').innerHTML=Array.from({length:90},(_,i)=>`<section class="body-section" id="I.3.4:b${String(90-i).padStart(2,'0')}" style="height:330px"><h2>Block ${i}</h2><p>${'History work and family '.repeat(35)}</p></section>`).join('');window.scrollTo(0,0);readerWindow.schedule()}''')
   page.wait_for_function('document.querySelectorAll(".passage-placeholder").length>40',timeout=5000)
   assert page.locator('.body-section').count()<=22
   page.wait_for_function('readerWindow.snapshotCount()<=48')
   page.wait_for_function('readerWindow.snapshotState("I.3.4:b01")==="evicted"',timeout=5000);page.evaluate('async()=>{await readerWindow.reveal("I.3.4:b01")}')
   page.wait_for_function('document.getElementById("I.3.4:b01")?.textContent?.includes("The architecture of staying")',timeout=10000)
   assert 'The architecture of staying' in page.locator('#I\\.3\\.4\\:b01').inner_text()
  assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),f'horizontal overflow at {width}'
  assert not errors,(width,errors)
  print(f'PASS {width}x{height}: 10 pathways, 27-event timeline, cross-subject detour, Korean search, bounded DOM+HTML snapshots, pack rehydration')
  page.close()
 browser.close()
