#!/usr/bin/env python3
"""Build network-loadable block assets from editable article source documents."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent.parent
out=ROOT/'data/blocks';out.mkdir(parents=True,exist_ok=True)
manifest=json.loads((ROOT/'data/content-manifest.json').read_text())
for entry in manifest['articles']:
    article=json.loads((ROOT/'data/articles'/f"{entry['id']}.json").read_text())
    paths=[]
    for block in article['blocks']:
        fn=block['id'].replace(':','-')+'.json'
        b=json.dumps(block,ensure_ascii=False,separators=(',',':')).encode('utf-8')
        (out/fn).write_bytes(b)
        paths.append({'id':block['id'],'title':block['title'],'path':'./data/blocks/'+fn,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
    entry['chunks']=paths
manifest['sampleWordCount']=sum(e['wordCount'] for e in manifest['articles'])
(ROOT/'data/content-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Produced',sum(len(e['chunks']) for e in manifest['articles']),'independently fetchable chunks')
