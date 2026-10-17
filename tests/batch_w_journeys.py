"""Batch W Chromium generated-asset acceptance (not a real HTTP origin)."""
import json,re
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
assets={'./data/'+f:json.loads((R/'data'/f).read_text()) for f in ['architecture.json','content-manifest.json','explore.json','atlas.json','search/catalog.json','search/shard-map.json']}
for folder in ('packs','search/shards'):
    for p in (R/'data'/folder).glob('*.json'):
        assets['./data/'+folder+'/'+p.name]=json.loads(p.read_text())
html=re.sub(r'<script type="module"[^>]+></script>','',re.sub(r'<link rel="stylesheet"[^>]+>','',(R/'index.html').read_text()))
js='\n'.join([(R/'exploration.js').read_text().replace('export ',''),(R/'content-platform.js').read_text().replace('export ','').replace("import {rankSearch} from './exploration.js';",''),(R/'reader-window.js').read_text().replace('export ',''),(R/'app.js').read_text().replace("import {rankSearch,collectionFor} from './exploration.js';",'').replace("import {createPackLoader,createShardedSearch} from './content-platform.js';",'').replace("import {createReaderWindow} from './reader-window.js';",'')])
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
    for w,h in ((1440,900),(390,844),(320,720)):
        page=browser.new_page(viewport={'width':w,'height':h})
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content(html);page.add_style_tag(content=(R/'styles.css').read_text())
        page.evaluate('items=>{window.fetch=async p=>({ok:!!items[p],status:items[p]?200:404,json:async()=>items[p]})}',assets)
        page.add_script_tag(content=js);page.wait_for_selector('.home-hero')
        for ch in ('VI.1','VII.1'):
            page.evaluate('id=>location.hash="#/chapter/"+id',ch);page.wait_for_selector('.chapter-complete')
            assert '10 available to read' in page.locator('.chapter-stats').inner_text()
            assert page.locator('.chapter-index .subchapter-btn').count()==10
            page.locator('.chapter-intro .btn-primary').click();page.wait_for_selector('.pathway-stop')
            assert page.locator('.pathway-stop').count()==10
        page.evaluate('location.hash="#/history/VI.1.1"')
        page.wait_for_selector('.passage-evidence')
        page.locator('.passage-evidence summary').first.click()
        assert 'National Institute of Korean History' in page.locator('.passage-evidence').first.inner_text()
        page.keyboard.press('/');page.locator('#searchInput').fill('조선 건국')
        page.wait_for_function('document.querySelector(".search-results")?.textContent.includes("VI.1.1")',timeout=20000)
        page.keyboard.press('Escape')
        page.evaluate('location.hash="#/history/VII.1.9"')
        page.wait_for_function('document.body.textContent.includes("The invasion arrives before full preparation")',timeout=20000)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),('horizontal overflow',w)
        assert not errors,(w,errors)
        page.close()
    browser.close()
print('PASS Batch W desktop/mobile generated assets: both full Chapters, two pathways, citation, Korean search, Joseon founding and Manchu invasions, zero pageerrors or horizontal overflow.')
