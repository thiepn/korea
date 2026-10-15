#!/usr/bin/env python3
"""Publish an annotated chronology and curated cross-topic connections.

The human-authored atlas is separate from immutable canonical architecture.
Verify every ID, avoid implied precision for broad date ranges, and avoid
inventing relationships by automatically joining all nearby IDs.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
source=json.loads((ROOT/'content/atlas/atlas.json').read_text(encoding='utf8'))
arch=json.loads((ROOT/'data/architecture.json').read_text(encoding='utf8'))
ids={s['id'] for p in arch['parts'] for c in p['chapters'] for s in c['subchapters']}
published={p.stem for p in (ROOT/'data/articles').glob('*.json')}
assert source['version']==1 and len(source['events'])>=20 and len(source['connections'])>=20
seen=set();last=-float('inf')
for e in source['events']:
 assert e['id'] in ids and e['id'].split('.')[0]==e['era'] and isinstance(e['year'],int)
 assert e['year']>=last,'Chronological sorting lost'
 last=e['year']
 assert len(e['title'])>=12 and len(e['detail'])>=55
 key=e['year'],e['id']
 assert key not in seen
 seen.add(key)
seen=set()
for link in source['connections']:
 assert link['from']!=link['to'] and link['from'] in ids and link['to'] in ids
 assert link['from'] in published and link['to'] in published, 'Connections must lead to readable content'
 assert len(link['why'])>=60
 pair=frozenset([link['from'],link['to']]);assert pair not in seen;seen.add(pair)
output=ROOT/'data/atlas.json'
output.write_text(json.dumps(source,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
print('PASS curated atlas:',len(source['events']),'events and',len(source['connections']),'explained connections')
