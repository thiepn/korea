#!/usr/bin/env python3
"""Prepare original Batch H chapter and append-only deepening through source-first JSONL.

No rewriting of existing paragraphs or shadow content engine. Source roles refer to
specific claims; the rest of each essay remains unreviewed editorial synthesis.
"""
from pathlib import Path
from prepare_editorial import prepare
from build_corpus import DATA,WORD_RE,canonical
import json,sys,re
ROOT=Path(__file__).resolve().parents[1]
VOLUME=ROOT/'content/editorial/batch_h_liberation_collection.md'
DEEP=ROOT/'content/editorial/batch_h_deepening.md'
SOURCES=ROOT/'content/research/batch_h_sources.json'
OUTPUT=ROOT/'content/imports/batch_h_collections.jsonl'
NEW={f'IX.1.{n}' for n in range(4,11)}
DEEPEN={'IX.1.1','IX.1.6','VI.4.3','IX.3.3','III.3.8'}

def parse_addenda(path:Path):
    allowed=canonical();articles=[];item=None;block=None
    for n,raw in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
        line=raw.strip()
        if line.startswith('## '):
            key=line[3:].strip()
            if key not in allowed:raise ValueError(f'unknown canonical addendum: {key}')
            item={'id':key,'mode':'append','blocks':[]};articles.append(item);block=None
        elif line.startswith('### '):
            if item is None:raise ValueError('orphan passage')
            block={'title':line[4:].strip(),'paragraphs':[]};item['blocks'].append(block)
        elif line and not line.startswith('#'):
            if item is None:continue
            if block is None:raise ValueError(f'orphan narrative line {n}')
            if len(WORD_RE.findall(line))<45:raise ValueError(f'inadequate addendum paragraph line {n}')
            block['paragraphs'].append(line)
    if len(set(a['id'] for a in articles))!=len(articles):raise ValueError('duplicate addendum ID')
    if any(not a['blocks'] or any(not b['paragraphs'] for b in a['blocks']) for a in articles):raise ValueError('empty addendum')
    return articles

def build():
    tmp=OUTPUT.with_suffix('.tmp')
    prepare(VOLUME,tmp,release='H',allow_existing=True)
    new=[json.loads(line) for line in tmp.read_text(encoding='utf-8').splitlines() if line]
    tmp.unlink()
    assert {x['id'] for x in new}==NEW
    deep=parse_addenda(DEEP)
    assert {x['id'] for x in deep}==DEEPEN
    registry=json.loads(SOURCES.read_text(encoding='utf-8'))
    assert set(registry['articles'])==NEW
    for a in new:
        item=registry['articles'][a['id']];refs=item['refs']
        a.update(description='One linked entry in Chapter IX.1, from liberation to divided state formation.',kicker='COMPLETE HISTORICAL CHAPTER',sourceStatus='Selective primary and Korean-language reference anchors; wider historical interpretation is original editorial synthesis, not academically peer-reviewed.',sources=[registry['references'][rid] for rid in refs])
        if len(a['blocks'])<3:raise ValueError('Insufficient article depth')
        for claim in item['claims']:
            b=a['blocks'][claim['passage']]
            b.setdefault('evidence',[]).append({k:v for k,v in claim.items() if k not in ('passage','source')}|{'sourceIndex':refs.index(claim['source'])})
    new_by_id={a['id']:a for a in new}
    # The existing IX.1.6 article is not yet in data/articles; fold the separately
    # authored long-form supplement into its first publication, preserving sequence.
    staged=[]
    for d in deep:
        if d['id'] in new_by_id:
            article=new_by_id[d['id']]
            article['blocks'].extend(d['blocks'])
            continue  # first-publication supplement remains part of the exact replay
        else:
            if not (DATA/'articles'/f"{d['id']}.json").exists():raise ValueError('Missing original article: '+d['id'])
            staged.append(d)
    data=new+staged
    OUTPUT.write_text(''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in data),encoding='utf-8')
    return {'new_articles':len(new),'deepened_prior_articles':len(staged),'passages':sum(len(x['blocks']) for x in data),'added_words':sum(len(WORD_RE.findall(p)) for a in data for b in a['blocks'] for p in b['paragraphs']),'evidence_anchors':sum(len(b.get('evidence',[])) for a in new for b in a['blocks'])}

if __name__=='__main__':
    try:print(json.dumps(build(),indent=2))
    except (ValueError,AssertionError,IndexError) as e:print('PREPARE FAILED',e,file=sys.stderr);sys.exit(1)
