#!/usr/bin/env python3
"""Compile Batch A thematic paths and corpus-aware search data from canonical IDs."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent.parent
arch=json.loads((ROOT/'data/architecture.json').read_text()); manifest=json.loads((ROOT/'data/content-manifest.json').read_text())
canonical={s['id'] for p in arch['parts'] for c in p['chapters'] for s in c['subchapters']}
collections=[
 ('everyday-worlds','Everyday worlds','What did the land, houses, food, and work of ordinary life demand from people?','The human scale',['I.1.4','II.1.7','IV.2.2','VI.1.3','VII.1.1','X.2.5']),
 ('power-and-legitimacy','Power and legitimacy','How did rulers persuade, recruit, challenge, and sometimes lose the people around them?','Courts and kingdoms',['II.1.2','III.1.5','V.1.5','VI.4.2','VIII.9.2','IX.1.2']),
 ('across-the-water','Across the water','Explore trade routes, maritime contact, diplomacy, and the movement of ideas.','Connections',['I.1.4','III.2.2','VIII.1.5','IX.1.2','X.5.10']),
 ('cities-and-society','Cities and society','From early settlement to digital cities: communities continually remake their environments.','Living places',['II.1.7','IV.2.2','VI.1.3','VII.1.1','IX.1.1','X.2.5']),
 ('moments-of-change','Moments of change','Follow crises, new political settlements, and the uncertain aftermath of pivotal events.','Turning points',['II.1.2','III.1.5','VII.1.1','VIII.9.2','IX.1.1','IX.1.2']),
 ('ideas-and-expression','Ideas and expression','Foundation stories, learning, writing, reform, and cultural influence.','Cultural history',['II.1.2','IV.2.2','V.1.5','VI.4.2','VIII.1.5','X.5.10']),
]
trails=[]
for slug,title,description,kicker,ids in collections:
 assert len(set(ids))==len(ids) and all(id in canonical for id in ids),slug
 trails.append(dict(slug=slug,title=title,description=description,kicker=kicker,ids=ids))
(ROOT/'data/explore.json').write_text(json.dumps({'version':1,'collections':trails},ensure_ascii=False,indent=2)+'\n')
search=[]
for item in manifest['articles']:
 article=json.loads((ROOT/'data/articles'/f"{item['id']}.json").read_text())
 blocks=[{'title':b['title'],'text':' '.join(b['paragraphs'])} for b in article['blocks']]
 search.append({'id':item['id'],'title':article['title'],'description':article['description'],'blocks':blocks})
(ROOT/'data/search-index.json').write_text(json.dumps({'version':1,'articleCount':len(search),'articles':search},ensure_ascii=False,separators=(',',':')))
print('PASS collections',len(trails),'and full-text sample index',len(search),'articles')
