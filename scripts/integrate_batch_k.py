#!/usr/bin/env python3
"""Use existing atlas, aliases, and route compiler for the Gojoseon complete chapter."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'content/atlas/atlas.json'
S=ROOT/'content/atlas/search-aliases.json'
C=ROOT/'scripts/build_exploration.py'
# The year is a sortable thematic/estimated position; the human-facing date explicitly
# identifies uncertainty. Do not claim an excavated Bronze Age object proves the kingdom.
EVENTS=[
 (-900,'Bronze Age, broad period','II.1.5','Liaoning and northern peninsula landscapes interact','The approximate marker introduces communities, rivers and routes later implicated in debates about Gojoseon; it is not a dated foundation event.'),
 (-800,'Bronze Age, broad period','II.1.9','Craft and ritual reshape community identities','Changing burial practices and prestige metalwork offer evidence for regional differentiation, without supplying a secure modern ethnic label.'),
 (-500,'First millennium BCE, broad period','II.1.3','Classical traditions about Gija acquire later afterlives','This thematic marker does not date a proven migration by Gija; it introduces the history of a contested origin claim.'),
 (-400,'Warring States era, approximately','II.1.6','Kingship and diplomatic claims enter transmitted accounts','Accounts quoted through later Chinese works describe kings, advisers and envoys, but do not offer a complete contemporary Gojoseon constitution.'),
 (-300,'Warring States era, broadly','II.1.8','The Joseon–Yan frontier becomes contested','Transmitted narratives describe a Yan advance associated with Qin Kai; the exact ancient boundary locations remain disputed.'),
 (-200,'Late first millennium BCE, broadly','II.1.7','Production and exchange sustain emerging political authority','Thematic landmark for farming, metalwork, storage and regional routes; not a precisely dated fiscal reform.'),
 (1281,'1281 CE (medieval source compilation)','II.1.10','Samguk yusa transmits a remembered foundation story','A medieval record gives access to the Dangun tradition, not eyewitness evidence for an exact Bronze Age foundation date.'),
]
CONNECTIONS=[
 ('I.4.2','II.1.1','The transition from chiefdom models to identifiable states shows why one named kingdom cannot be projected onto every earlier settlement.'),
 ('II.1.1','II.1.2','Evidence for a political formation and evidence for the medieval Dangun foundation tradition answer different historical questions.'),
 ('II.1.2','II.1.3','Dangun and Gija occupy different kinds of origin stories and gained different significance in later royal and intellectual memory.'),
 ('II.1.3','II.1.10','Gija traditions illuminate state ritual and Confucian historical imagination even when their Bronze Age migration claim lacks confirmation.'),
 ('II.1.4','II.1.5','Bronze dagger distributions inform regional geography but are not a reliable standalone map of a named kingdom.'),
 ('II.1.5','II.1.6','Control of river corridors and frontier relationships would have shaped how early rulers reached beyond their immediate communities.'),
 ('II.1.6','II.1.7','Political demands depended on food storage, workshops, exchange and households whose individual voices are not preserved.'),
 ('II.1.7','II.1.9','Production and craft specialists help us examine social diversity beyond weapons and diplomatic stories.'),
 ('II.1.8','II.1.6','Transmitted diplomatic disputes with Yan provide limited but valuable evidence of rulers, advisers and contested royal standing.'),
 ('II.1.8','II.2.1','The Yan frontier setting matters for understanding later migration and Wiman, without merging distinct generations into one episode.'),
 ('II.1.9','IV.3.2','Comparing social histories across very distant periods helps expose the limitations of each archive without assuming the same institutions.'),
 ('II.1.10','VI.4.3','The construction of a shared historical past and the creation of a vernacular writing system illuminate different ways states shaped cultural legitimacy.'),
]
ALIASES={
 'II.1.1':['고조선','고조선 역사','고조선 건국','고조선 국가 형성'],
 'II.1.2':['단군','단군신화','단군왕검','삼국유사'],
 'II.1.3':['기자조선','기자','기자 동래설','은나라 기자'],
 'II.1.4':['비파형동검','청동검','청동기 무덤','고조선 고고학'],
 'II.1.5':['요동','요령','요동 중심설','고조선 강역','고조선 위치'],
 'II.1.6':['조선후','고조선 왕권','고조선 정치','고조선 대부'],
 'II.1.7':['고조선 경제','고조선 농업','고조선 교역'],
 'II.1.8':['연나라','진개','고조선 연나라','전국시대'],
 'II.1.9':['예맥','고조선 사회','요령 묘제','고조선 주민'],
 'II.1.10':['고조선 사학사','단군기원','기자 숭배','고조선 역사인식'],
}

def run():
    atlas=json.loads(A.read_text(encoding='utf-8'))
    keys={(e['year'],e['id']) for e in atlas['events']}
    for year,date,id,title,detail in EVENTS:
        if (year,id) not in keys:atlas['events'].append(dict(year=year,date=date,era='II',id=id,title=title,detail=detail))
    atlas['events'].sort(key=lambda e:(e['year'],e['id']))
    pairs={frozenset((c['from'],c['to'])) for c in atlas['connections']}
    for a,b,why in CONNECTIONS:
        if frozenset((a,b)) not in pairs:atlas['connections'].append({'from':a,'to':b,'why':why})
    A.write_text(json.dumps(atlas,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    aliases=json.loads(S.read_text(encoding='utf-8'))
    for id,words in ALIASES.items():aliases[id]=sorted(set(aliases.get(id,[])+words))
    S.write_text(json.dumps(aliases,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    code=C.read_text(encoding='utf-8')
    needle=" ('ideas-and-expression','Ideas and expression'"
    replacement=" ('gojoseon-evidence-and-memory-complete','Gojoseon: archaeological evidence and historical memory','Ten connected studies compare Bronze Age evidence, transmitted Joseon–Yan encounters, contested origin traditions and later uses of antiquity.','Ten connected readings',[f'II.1.{i}' for i in range(1,11)]),\n"+needle
    if 'gojoseon-evidence-and-memory-complete' not in code:
        if needle not in code:raise ValueError('Missing route insertion point')
        C.write_text(code.replace(needle,replacement,1),encoding='utf-8')
    print(f'Batch K: {len(atlas["events"])} dated/thematic landmarks; {len(atlas["connections"])} explained links; 1 new complete route')
if __name__=='__main__':run()
