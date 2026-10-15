#!/usr/bin/env python3
"""Deterministic v2 KOREA corpus compiler. No network, dependencies or API costs.

Compiles editable data/articles/*.json into immutable content-addressed packs, a
small runtime article manifest, and a lazy full-text index sharded by token prefix.
Existing article IDs, block IDs, sequence and canonical source bytes are preserved.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
WORD_RE = re.compile(r"\b[\w’'-]+\b", re.UNICODE)
TOKEN_RE = re.compile(r'[a-z0-9]{3,}', re.ASCII)
STOP = set('the and for but was were are that this with from have has had into between its their there which what when where been being about also through these those they them then than would could should because while before after under over more some each other only such many much very even often across among most just will can not you your our how why who all his her she him one two three both onto itself within without together during around'.split())
MAX_PACK_BYTES = 24_000  # keep HTTP payloads bounded; browser downloads only 1 small pack


def encode(obj):
    return (json.dumps(obj, ensure_ascii=False, separators=(',', ':'), sort_keys=True) + '\n').encode('utf-8')


def digest(data: bytes):
    return hashlib.sha256(data).hexdigest()


def words(text):
    normalized = unicodedata.normalize('NFKD', text).casefold()
    return normalized.encode('ascii', 'ignore').decode('ascii')


def tokenize(text):
    return [w for w in TOKEN_RE.findall(words(text)) if w not in STOP]


def canonical():
    arch=json.loads((DATA/'architecture.json').read_text())
    result={s['id']:s['title'] for p in arch['parts'] for c in p['chapters'] for s in c['subchapters']}
    if len(result) != 1000: raise ValueError('Canonical v1.1 IDs are incomplete')
    return result


def compile_corpus(*, write=True):
    titles=canonical()
    articles=[]
    for f in sorted((DATA/'articles').glob('*.json')):
        a=json.loads(f.read_text(encoding='utf-8'))
        key=a.get('id')
        if key not in titles: raise ValueError(f'Unknown canonical article: {f.name}: {key}')
        if key+'.json' != f.name: raise ValueError(f'Filename / canonical ID mismatch: {f.name}')
        if a.get('title') != titles[key]: raise ValueError(f'Canonical title changed: {key}: {a.get("title")!r}')
        blocks=a.get('blocks')
        if not isinstance(blocks,list) or not blocks: raise ValueError(f'Empty article: {key}')
        seen=set()
        for i,b in enumerate(blocks,1):
            if b.get('id') != f'{key}:b{i:02d}' or b.get('sequence',i) != i or not b.get('title'):
                raise ValueError(f'Unstable passage identity / sequence in {key} at {i}')
            if b['id'] in seen or not isinstance(b.get('paragraphs'),list) or not b['paragraphs'] or any(not isinstance(p,str) or len(p.strip())<20 for p in b['paragraphs']):
                raise ValueError(f'Malformed / duplicate passage in {key} at {i}')
            seen.add(b['id'])
        articles.append(a)
    if not articles: raise ValueError('Refusing to publish an empty corpus')

    # A deterministic fixture to verify no changes on a second compile.
    manifest=[]; packs={}; catalog=[]; tokens={}; counted=0
    for a in articles:
        key=a['id']; passage_index=[]; groups=[]; current=[]
        def flush():
            if not current:return
            raw=encode({'version':2,'article':key,'blocks':list(current)})
            fn=f'{key}-{digest(raw)[:16]}.json'; path=f'./data/packs/{fn}'
            packs[fn]=raw
            for idx,b in enumerate(current):
                passage_index.append({'id':b['id'],'title':b['title'],'pack':path,'offset':idx,'sha256':digest(encode(b))})
            groups.append({'path':path,'sha256':digest(raw),'bytes':len(raw),'blocks':len(current)})
            current.clear()
        for block in a['blocks']:
            trial=encode({'version':2,'article':key,'blocks':current+[block]})
            if current and len(trial)>MAX_PACK_BYTES:flush()
            current.append(block)
        flush()
        count=sum(len(WORD_RE.findall(p)) for b in a['blocks'] for p in b['paragraphs']);counted+=count
        manifest.append({'id':key,'title':a['title'],'kicker':a.get('kicker','HISTORY'), 'description':a.get('description',''), 'wordCount':count,'blocks':len(a['blocks']), 'chunks':passage_index,'packs':groups})
        doc_index=len(catalog)
        catalog.append({'id':key,'title':a['title'],'description':a.get('description',''),'blocks':len(a['blocks']),'wordCount':count,'previews':[{'title':b['title'],'text':b['paragraphs'][0][:168].replace('\n',' ')} for b in a['blocks']]})
        for block_index,b in enumerate(a['blocks']):
            # One compact [document,passage] posting per article/term. No duplicated paragraphs.
            for paragraph in b['paragraphs']:
                seen_terms=set(tokenize(paragraph+' '+b['title']))
                for term in seen_terms:
                    index=tokens.setdefault(term,{})
                    if key not in index:index[key]=[doc_index,block_index]

    shards={}
    for term,items in sorted(tokens.items()):
        prefix=term[:2];shards.setdefault(prefix,{})[term]=list(items.values())
    shard_assets={}; shard_manifest={}
    for prefix,posting in shards.items():
        raw=encode({'version':2,'prefix':prefix,'terms':posting})
        filename=f'{prefix}-{digest(raw)[:12]}.json'
        path=f'./data/search/shards/{filename}'
        shard_assets[filename]=raw
        shard_manifest[prefix]={'path':path,'bytes':len(raw),'sha256':digest(raw)}
    result={'version':2,'count':len(manifest),'sampleWordCount':counted,'articles':manifest,'search':{'version':2,'catalog':'./data/search/catalog.json','shards':'./data/search/shard-map.json','totalTerms':len(tokens)}}
    shardmap={'version':2,'shards':shard_manifest,'articleCount':len(manifest)}
    changed=0
    if write:
        for folder in (DATA/'packs',DATA/'search/shards'): folder.mkdir(parents=True,exist_ok=True)
        # Content addressing preserves URLs for unaffected packs and shards.
        def ensure(path,raw):
            nonlocal changed
            if path.exists() and path.read_bytes()==raw:return
            temp=path.with_name(path.name+'.writing')
            temp.write_bytes(raw);temp.replace(path);changed+=1
        for name,raw in packs.items():ensure(DATA/'packs'/name,raw)
        for name,raw in shard_assets.items():ensure(DATA/'search/shards'/name,raw)
        for name,obj in [('content-manifest.json',result),('search/catalog.json',{'version':2,'articles':catalog}),('search/shard-map.json',shardmap)]:
            ensure(DATA/name,encode(obj))
        # Stale hashed products must not accidentally leak into the release output.
        for folder,needed in [(DATA/'packs',set(packs)),(DATA/'search/shards',set(shard_assets))]:
            for old in folder.glob('*.json'):
                if old.name not in needed:old.unlink();changed+=1

    return {'articles':len(manifest),'words':counted,'blocks':sum(len(a['blocks']) for a in articles),'packs':len(packs),'search_shards':len(shards),'terms':len(tokens),'largest_pack':max(map(len,packs.values())),'largest_shard':max(map(len,shard_assets.values())),'assets_changed':changed}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true',help='Check source corpus, do not write artifacts');args=ap.parse_args()
    print(json.dumps(compile_corpus(write=not args.check),indent=2))
