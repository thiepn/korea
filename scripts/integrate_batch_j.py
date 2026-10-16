#!/usr/bin/env python3
"""Curated sixth-Chapter reading routes, Korean discovery, and social-history cross-links.

Do not invent a precise date for the Silla Village Register; broad interpretive
chronology entries are explicitly marked approximate in both labels and descriptions.
"""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
A=R/'content/atlas/atlas.json'
S=R/'content/atlas/search-aliases.json'
C=R/'scripts/build_exploration.py'
EVENTS=[
 (674,'674 CE','IV.3.8','Wolji is created near the Silla royal residence','An elite palace pond, dated by transmitted texts and interpreted through excavation, becomes an unusually rich material-culture site; the objects are not a cross-section of all households.'),
 (700,'Unified Silla, roughly 7th–9th centuries','IV.3.2','Households underpin the expanded kingdom','This thematic landmark has no single dated event: household labor, kinship and unequal status sustained the society documented only selectively in administrative and later textual sources.'),
 (730,'Unified Silla, date contested','IV.3.3','A village administration counts residents and resources','The Silla Village Register for four Seowongyeong-area communities survives by reuse; its composition date is disputed and should not be pinned to the illustrative timeline year.'),
 (735,'Unified Silla, date contested','IV.3.5','Land, livestock and trees enter fiscal categories','The village register lists fields, animals and productive trees, but its exact date and the institutional meanings of particular field labels remain matters of research.'),
 (745,'Unified Silla, thematic period','IV.3.6','Skilled production supports capital and countryside','Ceramics, cloth, metalwork, construction and repair supplied both grand patronage and routine household requirements; the marker is thematic, not a claimed single event.'),
 (828,'828 CE','IV.3.7','Cheonghaejin anchors a maritime route','The establishment of the naval-trade center under Jang Bogo is recorded for 828; subsequent biographies present a more complex transmitted narrative of his motives and leadership.'),
]
CONNECTIONS=[
 ('III.3.7','IV.3.5','Military expansion and stronger royal institutions intensified questions about how fields, local labor and assessed resources supported Silla’s extended political reach.'),
 ('III.3.8','IV.3.2','The language of aristocratic bone rank explains some royal marriage politics but cannot stand in for the social arrangements of ordinary Silla households.'),
 ('IV.3.1','IV.3.2','Fiscal household counts bring dependents and enslaved people into view, showing that social hierarchy continued within domestic relations as well as formal offices.'),
 ('IV.3.2','IV.3.3','A family’s options were shaped by the administrative villages that counted its members, documented movements and connected it to state obligations.'),
 ('IV.3.3','IV.3.5','The four surviving village records measure both residents and fields, making land distribution inseparable from the state’s knowledge of rural households.'),
 ('IV.3.4','IV.3.5','Agricultural productivity depended on water, terrain and labor, which complicate any interpretation of fiscal field categories as simple modern ownership.'),
 ('IV.3.4','IV.3.9','Crop production, irrigation, livestock and food availability shaped households’ ability to withstand shortages without providing a quantifiable epidemic record.'),
 ('IV.3.5','IV.3.6','Land, patrons and productive resources helped support specialist craftsmen and major religious buildings, although individual labor arrangements are rarely recorded.'),
 ('IV.3.6','IV.3.7','Commerce moved objects created by artisans and household workers; long-distance exchange depended on the organization of production at many local sites.'),
 ('IV.3.6','IV.3.8','Court objects and building materials reveal technical skill, but their elite archaeological contexts cannot be treated as typical of every dwelling.'),
 ('IV.3.7','IV.3.8','Capital demand, roads and maritime traffic connect imported courtly goods with a larger commercial world, though access was highly unequal.'),
 ('IV.3.9','IV.3.10','Seasonal illness and food insecurity formed part of the background against which labor, celebration, pilgrimage and family obligations were experienced.'),
 ('IV.3.2','IV.3.10','The retrospectively recorded Gabae weaving festival joins gendered labor, household production and communal celebration without documenting every village custom.'),
 ('IV.3.7','V.5.6','Maritime exchange, the circulation of texts and the labor behind religious copying anticipate questions about how later Korean Buddhist scholarship moved across regions.'),
]
ALIASES={
 'IV.3.2':['신라 가족','신라 혼인','신라 여성','가족과 친족','신라 가구'],
 'IV.3.5':['신라 토지','전답','신라촌락문서','장적','신라 토지 제도'],
 'IV.3.6':['신라 수공업','도공','금속 공예','직조','공방'],
 'IV.3.7':['신라 시장','경주 시장','청해진','장보고','해상무역'],
 'IV.3.8':['동궁과 월지','안압지','신라 왕경','신라 생활','신라 복식'],
 'IV.3.9':['신라 기근','신라 질병','인구 이동','전염병','신라 보건'],
 'IV.3.10':['가배','신라 명절','회소곡','신라 유희','신라 축제'],
 'IV.3.1':['신라 신분','노비','골품','신라 계층'],
 'IV.3.3':['신라 촌락','서원경','신라 장적','민정 문서'],
 'IV.3.4':['신라 벼농사','논농사','밭농사','신라 농업','수리시설'],
}
def run():
 atlas=json.loads(A.read_text(encoding='utf8'))
 seen={(e['year'],e['id']) for e in atlas['events']}
 for year,date,id,title,detail in EVENTS:
  if (year,id) not in seen:atlas['events'].append(dict(year=year,date=date,era='IV',id=id,title=title,detail=detail))
 atlas['events'].sort(key=lambda e:(e['year'],e['id']))
 pairs={frozenset((c['from'],c['to'])) for c in atlas['connections']}
 for a,b,why in CONNECTIONS:
  if frozenset((a,b)) not in pairs:atlas['connections'].append(dict(**{'from':a,'to':b,'why':why}))
 A.write_text(json.dumps(atlas,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 aliases=json.loads(S.read_text(encoding='utf8'))
 for id,words in ALIASES.items():aliases[id]=sorted(set(aliases.get(id,[])+words))
 S.write_text(json.dumps(aliases,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 code=C.read_text(encoding='utf8')
 old=" ('ideas-and-expression','Ideas and expression'"
 new=" ('silla-everyday-life-complete','Silla: everyday lives and unequal opportunities','Ten connected studies of households, fields, craft, trade, cities, health and leisure beyond the royal court.','Ten connected readings',[f'IV.3.{i}' for i in range(1,11)]),\n ('ideas-and-expression','Ideas and expression'"
 if 'silla-everyday-life-complete' not in code:
  if old not in code:raise ValueError('Expected existing exploration collection insertion point absent')
  C.write_text(code.replace(old,new,1),encoding='utf8')
 print(f'Batch J atlas: {len(atlas["events"])} landmarks, {len(atlas["connections"])} explained connections, {len(ALIASES)} alias groups enriched')
if __name__=='__main__':run()
