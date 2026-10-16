#!/usr/bin/env python3
"""Compile two original editorial Chapter collections through the existing importer.

The result is deterministic, replay-safe and keeps source-level evidence annotations
separate from claims of whole-essay academic verification.
"""
from pathlib import Path
import sys,json,re,urllib.parse
from prepare_editorial import prepare
from build_corpus import DATA,WORD_RE,canonical
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'content/imports/batch_f_collections.jsonl'
REGISTRY=ROOT/'content/research/batch_f_sources.json'
INPUTS=[ROOT/'content/editorial/batch_f_hangul_collection.md',ROOT/'content/editorial/batch_f_war_collection.md']
EXPECTED={f'VI.4.{n}' for n in range(5,11)}|{f'IX.3.{n}' for n in range(5,11)}

def build(write=True):
    data=json.loads(REGISTRY.read_text(encoding='utf-8'))
    assert set(data['articles'])==EXPECTED
    items=[]
    for file in INPUTS:
        scratch=OUT.with_suffix('.tmp')
        prepare(file,scratch,dry_run=False,release='F',allow_existing=True)
        items.extend(json.loads(line) for line in scratch.read_text(encoding='utf-8').splitlines() if line)
        scratch.unlink()
    if {item['id'] for item in items}!=EXPECTED or len(items)!=12:raise ValueError('Incomplete or duplicate Chapter coverage')
    words_total=0
    for item in items:
        key=item['id'];meta=data['articles'][key]
        words=sum(len(WORD_RE.findall(p)) for b in item['blocks'] for p in b['paragraphs'])
        if words<480 or len(item['blocks'])<3 or any(len(b['paragraphs'])<2 for b in item['blocks']):raise ValueError(f'Insufficient independent content: {key} ({words} words)')
        if (DATA/'articles'/f'{key}.json').exists():
            # Build must be replayable against the committed article, not a replacement.
            pass
        words_total+=words
        item.update(description='An original sustained chapter collection entry; specific reference-backed facts are marked per passage and interpretations remain editorial synthesis.',kicker='COLLECTED HISTORICAL READING',sourceStatus='Selected passage-level factual anchors checked against named institutional resources; remaining prose is editorial interpretation, not independently peer-reviewed.',sources=[data['references'][id] for id in meta['refs']])
        for claim in meta['claims']:
            i=claim['passage']
            if i>=len(item['blocks']) or claim['source'] not in meta['refs']:raise ValueError('Invalid claim anchor '+key)
            src=meta['refs'].index(claim['source'])
            item['blocks'][i].setdefault('evidence',[]).append({'claim':claim['claim'],'sourceIndex':src,'locator':claim['locator'],'type':claim['type']})
    result=''.join(json.dumps(i,ensure_ascii=False,separators=(',',':'))+'\n' for i in items)
    if write:OUT.write_text(result,encoding='utf-8')
    return {'articles':len(items),'passages':sum(len(i['blocks']) for i in items),'words':words_total,'marked_claims':sum(len(m['claims']) for m in data['articles'].values())}

if __name__=='__main__':
    try:print(json.dumps(build(),indent=2))
    except Exception as e:print('Collection validation failed:',str(e),file=sys.stderr);sys.exit(1)
