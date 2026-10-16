"""Chromium desktop/mobile interaction against exact built assets, not live origin."""
import json,re
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
assets={'./data/'+f:json.loads((R/'data'/f).read_text()) for f in ['architecture.json','content-manifest.json','explore.json','atlas.json','search/catalog.json','search/shard-map.json']}
for folder in ('packs','search/shards'):
 for p in (R/'data'/folder).glob('*.json'):assets['./data/'+folder+'/'+p.name]=json.loads(p.read_text())
html=re.sub(r'<script type="module"[^>]+></script>','',re.sub(r'<link rel="stylesheet"[^>]+>','',(R/'index.html').read_text()))
js='\n'.join([(R/'exploration.js').read_text().replace('export ',''),(R/'content-platform.js').read_text().replace('export ','').replace("import {rankSearch} from './exploration.js';",''),(R/'reader-window.js').read_text().replace('export ',''),(R/'app.js').read_text().replace("import {rankSearch,collectionFor} from './exploration.js';",'').replace("import {createPackLoader,createShardedSearch} from './content-platform.js';",'').replace("import {createReaderWindow} from './reader-window.js';",'')])
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 for w,h in [(1440,900),(390,844),(320,720)]:
  page=browser.new_page(viewport={'width':w,'height':h});errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(html);page.add_style_tag(content=(R/'styles.css').read_text())
  page.evaluate('assets=>{window.fetch=async p=>({ok:!!assets[p],status:assets[p]?200:404,json:async()=>assets[p]})}',assets)
  page.add_script_tag(content=js);page.wait_for_selector('.home-hero')
  for chapter in ['V.5','VIII.9']:
   page.evaluate('x=>location.hash="#/chapter/"+x',chapter);page.wait_for_selector('.chapter-complete')
   assert '10 available to read' in page.locator('.chapter-stats').inner_text()
   assert page.locator('.chapter-index .subchapter-btn').count()==10
   page.locator('.chapter-intro .btn-primary').click();page.wait_for_selector('.pathway-stop')
   assert page.locator('.pathway-stop').count()==10
  page.evaluate('location.hash="#/history/V.5.3"');page.wait_for_function('document.body.textContent.includes("A prince who treated commentaries")')
  assert page.locator('.passage-evidence').count()>=1
  page.locator('.passage-evidence summary').first.click()
  assert 'National Institute of Korean History' in page.locator('.passage-evidence').first.inner_text()
  page.keyboard.press('/');page.locator('#searchInput').fill('의천')
  page.wait_for_function('document.querySelector(".search-results")?.textContent.includes("V.5.3")',timeout=16000)
  page.keyboard.press('Escape')
  page.evaluate('location.hash="#/history/VIII.9.3"');page.wait_for_function('document.body.textContent.includes("What does a republic mean")')
  assert page.locator('.passage-evidence').count()>0
  page.evaluate('location.hash="#/timeline"');page.wait_for_selector('.timeline-page')
  assert 'Singanhoe' in page.locator('body').inner_text()
  if not page.evaluate('document.documentElement.scrollWidth<=innerWidth'):
   print('OVERFLOW',w,page.evaluate('({w:innerWidth,scroll:document.documentElement.scrollWidth,els:[...document.querySelectorAll("*")].map(e=>({tag:e.tagName,cl:e.className,txt:e.textContent.slice(0,50),right:e.getBoundingClientRect().right,left:e.getBoundingClientRect().left})).filter(x=>x.right>innerWidth+2).slice(0,16)})'))
  if w==320:print('WIDE BOXES',page.evaluate('[...document.querySelectorAll("*")].filter(e=>e.scrollWidth>e.clientWidth+4 && e.clientWidth>0).map(e=>[e.tagName, e.className, e.clientWidth,e.scrollWidth]).slice(0,20)'))
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'overflow {w}'
  assert not errors,errors
  print(f'PASS Chromium {w}x{h}: 2 complete chapter routes; evidence; Korean search; chronology; mobile layout')
  page.close()
 browser.close()
