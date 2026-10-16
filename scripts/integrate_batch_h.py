#!/usr/bin/env python3
"""Deterministic, idempotent Batch H curated discovery integration."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
ATLAS=ROOT/'content/atlas/atlas.json';ALIASES=ROOT/'content/atlas/search-aliases.json'
EVENTS=[
 ('August–November 1945',1945,'IX.1.4','Local people’s committees emerge','Local committees respond to the vacuum left by Japanese surrender, claiming authority over safety and public administration while occupying powers approach.'),
 ('Autumn 1945',1945,'IX.1.5','Northern occupation and local governing bodies','Soviet commanders recognize and reshape northern provincial bodies while Korean political organizations compete to define a new order.'),
 ('September 1945',1945,'IX.1.6','US military government begins in the south','American military government succeeds Japanese colonial administration south of the 38th parallel amid disputes over which Korean organizations speak legitimately.'),
 ('Late 1945',1945,'IX.1.7','Exiled leaders return to an unsettled political stage','The return of Provisional Government figures and other exiles intensifies debates about national representation without settling who controls the administration.'),
 ('1945–1947',1946,'IX.1.8','Repatriation and shortages reshape daily life','Returning migrants, broken trade routes, changing wages and food distribution turn postwar reconstruction into an immediate political question.'),
 ('September–October 1946',1946,'IX.1.9','Strikes and the October unrest','Labor protests and unrest around Daegu connect food insecurity, police authority and political rivalry across the southern occupation zone.'),
 ('1947–1948',1947,'IX.1.10','The Korean question goes to the United Nations','The failure of bilateral negotiations shifts proposed elections and national government formation toward UN deliberations; the commission lacks full territorial access.'),
]
CONNECTIONS=[
 ('IX.1.1','IX.1.4','Local committees attempted to turn the joy of liberation into working administration, before an accepted national government existed.'),
 ('IX.1.2','IX.1.5','The military boundary enabled distinct northern administrative decisions and reshaped local political organizations as occupation continued.'),
 ('IX.1.3','IX.1.4','The Committee for the Preparation of Korean Independence and the People’s Republic must be distinguished from varied local committees and their practical roles.'),
 ('IX.1.4','IX.1.6','Local self-government claims collided with US military-government decisions about recognized authority, police, and administrative personnel.'),
 ('IX.1.5','IX.1.10','Northern political institutions developed while the US–Soviet attempt to agree on a single Korean national settlement stalled.'),
 ('IX.1.6','IX.1.7','Formal authority remained with the military government even when returning exile figures and Korean political parties claimed representative legitimacy.'),
 ('IX.1.7','IX.1.10','The struggle among returning leaders and local factions shaped reactions to trusteeship, negotiations and an eventual divided electoral process.'),
 ('IX.1.8','IX.1.9','Food scarcity, wages, police conduct and disrupted livelihoods formed material contexts for the 1946 strikes and autumn unrest.'),
 ('IX.1.9','IX.1.10','Escalating conflict within the southern zone narrowed the room for domestic compromise while international negotiations continued to fail.'),
 ('IX.1.10','IX.3.1','The unresolved division of governments formed part of the Korean War’s political prehistory, although invasion was not an inevitable outcome of 1948.'),
 ('IX.1.10','X.1.2','The constitutional and political institutions established in the south after occupation influenced later debates about civilian government and democracy.'),
]
ALIAS_NEW={
'IX.1.4':['인민위원회','지방 자치','해방 직후 위원회'],
'IX.1.5':['소련군정','북한 점령','북조선 임시인민위원회'],
'IX.1.6':['미군정','미군정청','재조선미육군사령부군정청'],
'IX.1.7':['임시정부 환국','김구 귀국','해방 정당'],
'IX.1.8':['귀환동포','해방 후 식량난','미군정 원조'],
'IX.1.9':['대구 10월 사건','십일사건','1946년 10월 항쟁'],
'IX.1.10':['신탁통치','미소공동위원회','유엔 한국문제','남북 분단'],
}
def run():
    atlas=json.loads(ATLAS.read_text(encoding='utf8'));existing={(e['year'],e['id']) for e in atlas['events']}
    for date,year,key,title,detail in EVENTS:
        if (year,key) not in existing:
            atlas['events'].append({'date':date,'year':year,'era':'IX','id':key,'title':title,'detail':detail})
    atlas['events'].sort(key=lambda x:(x['year'],x['id']))
    pairs={frozenset((a['from'],a['to'])) for a in atlas['connections']}
    for source,target,why in CONNECTIONS:
        if frozenset((source,target)) not in pairs:
            atlas['connections'].append({'from':source,'to':target,'why':why})
    ATLAS.write_text(json.dumps(atlas,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    aliases=json.loads(ALIASES.read_text(encoding='utf8'))
    for key,values in ALIAS_NEW.items():
        aliases[key]=sorted(set(aliases.get(key,[])+values))
    ALIASES.write_text(json.dumps(aliases,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(f'Batch H atlas: {len(atlas["events"])} events; {len(atlas["connections"])} connections; {len(ALIAS_NEW)} enriched aliases')
if __name__=='__main__':run()
