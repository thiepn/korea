"""Browser smoke tests using an in-memory same-page asset adapter.
This executes actual app JS/CSS in Chromium but does NOT prove HTTP-origin or CDN behavior.
Run: python tests/browser_smoke.py (requires playwright and installed Chromium).
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,re,sys
R=Path(__file__).resolve().parent.parent
A={'./data/architecture.json':json.loads((R/'data/architecture.json').read_text()), './data/content-manifest.json':json.loads((R/'data/content-manifest.json').read_text())}
for f in (R/'data/blocks').glob('*.json'):
    A['./data/blocks/'+f.name]=json.loads(f.read_text())
html=re.sub(r'<script type="module"[^>]+></script>','',re.sub(r'<link rel="stylesheet"[^>]+>','',(R/'index.html').read_text()))
css=(R/'styles.css').read_text();js=(R/'app.js').read_text()
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    results=[]
    for width,height in [(1440,900),(390,844),(320,720),(844,390)]:
        pg=browser.new_page(viewport={'width':width,'height':height})
        errors=[];pg.on('pageerror',lambda exc: errors.append(str(exc)))
        pg.set_content(html);pg.add_style_tag(content=css)
        pg.evaluate('assets => {window.__assets=assets;window.fetch=async p=>({ok:!!window.__assets[p],status:window.__assets[p]?200:404,json:async()=>window.__assets[p]})}',A)
        pg.add_script_tag(content=js);pg.wait_for_selector('.home-hero')
        assert pg.locator('.era-card').count()==10
        assert pg.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'Homepage overflow {width}'
        pg.evaluate('location.hash="#/part/VI"');pg.wait_for_selector('.chapter-row')
        assert pg.locator('.chapter-row').count()==10
        assert pg.locator('.subchapter-btn').count()==10
        pg.locator('[data-action=chapter][data-id="VI.2"]').click()
        assert pg.locator('.subchapter-btn').count()==20
        pg.evaluate('location.hash="#/history/VI.4.2.1.2"');pg.wait_for_selector('.reader-title')
        assert 'Terminal subsection' in pg.locator('.reader-title').inner_text()
        assert '100 planned destinations' not in pg.locator('.reader-main').inner_text() # terminal shows parent link only
        pg.evaluate('location.hash="#/history/VI.4.2"');pg.wait_for_selector('.body-section')
        assert pg.locator('.body-section').count()==1
        pg.locator('[data-action=load-more]').click();pg.wait_for_function('document.querySelectorAll(".body-section").length===2')
        pg.locator('[data-action=bookmark]').click();assert pg.locator('.reader-action.saved').count()==1
        pg.locator('[data-action=settings]').click();assert pg.locator('.reader-toolbar-sub').count()==1
        pg.locator('[data-action=width][data-value="610"]').click()
        assert pg.evaluate('getComputedStyle(document.documentElement).getPropertyValue("--reader-width").trim()')=='610px'
        pg.locator('[data-action=mode][data-mode="overview"]').click();pg.wait_for_selector('.overview-topics')
        assert pg.locator('.overview-link').count()==4
        pg.locator('.overview-link').nth(2).click();pg.wait_for_selector('.body-section')
        pg.wait_for_function('document.querySelectorAll(".body-section").length>=3')
        pg.keyboard.press('/');pg.wait_for_selector('#searchInput')
        pg.locator('#searchInput').fill('Gwanggaeto'); assert pg.locator('.search-results button').count()>0
        pg.keyboard.press('Escape');assert pg.locator('.search-dialog').count()==0
        pg.evaluate('location.hash="#/saved"');pg.wait_for_selector('.saved-page')
        assert pg.locator('.saved-list .saved-row').count()>=1
        pg.evaluate('location.hash="#/history/III.1.5"');pg.wait_for_selector('.body-section')
        pg.locator('[data-action=mode][data-mode="endless"]').click();pg.wait_for_selector('.body-section')
        pg.locator('[data-action=load-more]').click();pg.wait_for_function('document.querySelectorAll(".body-section").length>=2')
        assert not errors,errors
        assert pg.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'Reader overflow {width}'
        results.append(f'PASS {width}x{height}: hierarchy, planned IDs, reader, progressive loading, search, saved, settings, modes')
        pg.close()
    browser.close()
print('\n'.join(results))
print('NOTE: In-memory assets; HTTP-origin browser behavior and actual deployment NOT TESTED.')
