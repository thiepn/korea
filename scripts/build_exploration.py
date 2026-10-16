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
 ('new-voices-of-the-archive','New voices of the archive','Newly written stories from fields, politics, households and changing workplaces.','Growing archive',['I.3.4','II.3.4','III.3.2','IV.3.3','V.2.5','VI.2.5','VII.3.4','VIII.3.5','IX.3.2','X.2.4']),
 ('fields-and-households','Fields and households','A route through shelter, farming, obligations and changing family life.','The human scale',['I.3.4','I.4.2','IV.3.3','V.3.5','VII.5.2','X.2.4']),
 ('learning-and-service','Learning and service','Why societies sought educated officials, and who had the chance to become one.','Education and power',['V.2.5','VI.4.2','VI.2.5','VII.3.4','X.1.2']),
 ('institutions-in-motion','Institutions in motion','From early commanderies to civilian democracy, trace how authority changes.','Power over time',['II.3.4','III.3.2','III.3.5','V.2.5','VI.2.5','VIII.3.5','X.1.2']),
 ('longform-history','The long history behind the headline','Read substantial essays, inspect their reference notes, and follow why one century raises questions for another.','Reading in depth',['V.5.6','VI.4.3','IX.3.3','VI.4.2','V.3.5','IX.3.2']),
 ('writing-and-knowledge','Hangul: the complete Chapter','Follow ten connected readings from Korean writing before Hangul to the earliest writing debates, books, and spelling practices.','Ten connected readings',[f'VI.4.{i}' for i in range(1,11)]),
 ('the-korean-war-complete','The Korean War: the complete Chapter','Read ten connected subjects from the outbreak through coalition warfare, civilian survival and the armistice.','Ten connected readings',[f'IX.3.{i}' for i in range(1,11)]),
 ('silla-rise-complete','Silla: the complete rise of a kingdom','Ten connected histories from fourth-century uncertainty through political reform, Jinheung’s expansion, queenship and the coalition of Chunchu and Yushin.','Ten connected readings',[f'III.3.{i}' for i in range(1,11)]),
 ('ideas-and-expression','Ideas and expression','Foundation stories, learning, writing, reform, and cultural influence.','Cultural history',['II.1.2','IV.2.2','V.1.5','VI.4.2','VIII.1.5','X.5.10']),
]
trails=[]
for slug,title,description,kicker,ids in collections:
 assert len(set(ids))==len(ids) and all(id in canonical for id in ids),slug
 trails.append(dict(slug=slug,title=title,description=description,kicker=kicker,ids=ids))
(ROOT/'data/explore.json').write_text(json.dumps({'version':1,'collections':trails},ensure_ascii=False,indent=2)+'\n')
print(f'PASS exploration: {len(trails)} canonical pathways; v2 searchable content compiled by build_corpus.py')
