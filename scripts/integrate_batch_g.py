#!/usr/bin/env python3
"""Idempotent integration of Batch G curated discovery metadata, not canonical edits."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
ATLAS=ROOT/'content/atlas/atlas.json'
ALIAS=ROOT/'content/atlas/search-aliases.json'
EVENTS=[
 ('c. 356 CE',356,'III.3.1','Silla in a changing eastern peninsula','The Kim royal line develops a firmer centre around Gyeongju, amid shifting aristocratic allegiances.'),
 ('400 CE',400,'III.3.3','The Goguryeo intervention','The Gwanggaeto inscription records Silla requesting support and Goguryeo entering the southern conflict.'),
 ('Fifth century CE',465,'III.3.4','A century of growing independence','Elites, diplomacy and political organization gradually increase Silla’s room to act beyond Goguryeo’s influence.'),
 ('c. 550s CE',550,'III.3.7','Jinheung and the Han River campaigns','Royal expansion brings Silla into the central peninsula; steles publicize authority and newly claimed territory.'),
 ('Sixth century CE',575,'III.3.8','The political order of bone rank','Inherited social status and aristocratic privilege structure access to office and the conflicts of succession.'),
 ('632–647 CE',632,'III.3.9','Seondeok’s reign and a challenged court','Military pressure, diplomatic initiatives, ambitious sacred construction and revolt mark the years of a Silla queen.'),
 ('654 CE',654,'III.3.10','Kim Chunchu becomes King Muyeol','An alliance of royal lineage, military strength and diplomacy prepares the kingdom for new campaigns and conflicts.'),
]
LINKS=[
 ('III.3.1','III.3.2','Silla’s emerging royal centre supplies the contested setting in which maripgan leadership and Kim-family succession gained prominence.'),
 ('III.3.2','III.3.3','The consolidation associated with Naemul did not prevent the dangerous appeal for Goguryeo support around the year 400.'),
 ('III.3.3','III.3.4','The rescue of 400 created political dependence; the following century shows how rulers sought greater room to act independently.'),
 ('III.3.4','III.3.5','Fifth-century networks and elite consolidation supplied the foundations for the named institutional changes under Jijeung.'),
 ('III.3.5','III.3.7','New public titles and forms of rule helped Silla turn a southeastern court into a state able to claim territories much farther away.'),
 ('III.3.6','III.3.7','Beopheung’s legal and religious projects provide context for the military ambition and royal monument building of Jinheung’s reign.'),
 ('III.3.7','III.3.8','Territorial growth increased both royal resources and aristocratic competition within the inherited bone-rank hierarchy.'),
 ('III.3.8','III.3.9','Hereditary rank made Seondeok’s succession possible while also giving rivals powerful languages for disputing her authority.'),
 ('III.3.9','III.3.10','The losses and elite conflicts of Seondeok’s reign changed the strategic choices that Kim Chunchu and Kim Yushin inherited.'),
 ('III.3.10','IV.3.1','The ruling coalition that expanded Silla cannot be understood apart from the social hierarchy and dependent labour of its society.'),
 ('III.3.7','IV.3.3','Royal conquests transformed the obligations of local communities; farmers and villages bore practical consequences of wider control.'),
]
ALIAS_NEW={
 'III.3.1':['신라 4세기','초기 신라','사로국'],
 'III.3.3':['광개토대왕 신라 구원','광개토왕릉비','신라 400년'],
 'III.3.4':['신라 5세기','경주 금관','신라 독립'],
 'III.3.7':['진흥왕','순수비','한강 유역 신라'],
 'III.3.8':['골품제','성골 진골','신라 귀족'],
 'III.3.9':['선덕여왕','비담의 난','황룡사 구층목탑'],
 'III.3.10':['김춘추','김유신','태종무열왕'],
}

def apply():
 atlas=json.loads(ATLAS.read_text(encoding='utf-8'));old=len(atlas['events']);con=len(atlas['connections'])
 present={(x['year'],x['id']) for x in atlas['events']}
 for date,year,key,title,detail in EVENTS:
  if (year,key) not in present:atlas['events'].append(dict(date=date,year=year,era='III',id=key,title=title,detail=detail))
 atlas['events'].sort(key=lambda e:(e['year'],e['id']))
 pairs={frozenset((x['from'],x['to'])) for x in atlas['connections']}
 for src,dest,why in LINKS:
  if frozenset((src,dest)) not in pairs:atlas['connections'].append({'from':src,'to':dest,'why':why})
 ATLAS.write_text(json.dumps(atlas,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 a=json.loads(ALIAS.read_text(encoding='utf8'))
 for key,terms in ALIAS_NEW.items():a[key]=terms
 ALIAS.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 print('Timeline',old,'->',len(atlas['events']),'connections',con,'->',len(atlas['connections']))
if __name__=='__main__':apply()
