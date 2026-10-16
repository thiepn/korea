#!/usr/bin/env python3
"""Curated links for the fifth complete Chapter. No new canonical identities."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=R/'content/atlas/atlas.json'; data=json.loads(p.read_text(encoding='utf-8'))
new_events=[
 (371,'371 CE','III.2.1','Baekje confronts Goguryeo in the north','Accounts associate the fourth-century campaign with Goguryeo King Gogukwon’s death; a later chronicle is not a complete military record.'),
 (475,'475 CE','III.2.6','Hanseong falls, royal center moves south','The death of King Gaero and relocation to Ungjin mark a profound strategic and political rupture for Baekje.'),
 (501,'501–523 CE','III.2.8','The reign of King Muryeong','The rebuilding Ungjin monarchy acquires unusually firm dates through his later excavated royal inscriptions.'),
 (523,'523 CE','III.2.8','King Muryeong dies','His primary funerary inscription records the date of death, with formal burial following in 525.'),
 (538,'538 CE','III.2.9','Capital transferred to Sabi','King Seong’s deliberate relocation toward present-day Buyeo forms part of renewed administrative and political ambition.'),
 (554,'554 CE','III.2.9','King Seong dies during conflict with Silla','The struggle over former Han River territories ended in another dynastic military crisis.'),
 (660,'660 CE','III.2.10','The Sabi kingdom falls','Silla and Tang campaigns end independent Baekje kingship; resistance in former Baekje territory continues afterward.'),
]
seen={(x['year'],x['id']) for x in data['events']}
for year,date,key,title,detail in new_events:
    if (year,key) in seen:continue
    data['events'].append({'date':date,'year':year,'era':'III','id':key,'title':title,'detail':detail})
data['events'].sort(key=lambda e:(e['year'],e['id']))
new_links=[
 ('III.2.1','III.2.2','The fourth-century Han basin sets the conditions for Geunchogo’s expansion while clarifying what later royal victory narratives leave unstated.'),
 ('III.2.2','III.2.3','Royal military success depended on a court landscape capable of coordinating people, wealth and political recognition in Hanseong.'),
 ('III.2.3','III.2.4','The early capital’s administrative prestige was reinforced by overseas embassies and the learned practices of East Asian courts.'),
 ('III.2.4','III.2.5','Connections with Chinese dynasties belonged to a wider maritime world that also linked Baekje and polities in the Japanese archipelago.'),
 ('III.2.5','III.2.6','After Hanseong’s fall, diplomatic and maritime networks became resources through which the displaced monarchy might seek renewed security.'),
 ('III.2.6','III.2.7','The forced departure from Hanseong explains why the Ungjin capital required new partners, new infrastructure and repeated political accommodation.'),
 ('III.2.7','III.2.8','Muryeong’s dated royal tomb provides material and written evidence for the later recovery of court dignity and international contact.'),
 ('III.2.8','III.2.9','The stability expressed by Muryeong’s burial helps frame the different political ambition of Seong’s planned move to Sabi.'),
 ('III.2.9','III.2.10','Sabi’s institutional and artistic achievements continued within strategic competition that culminated in the campaigns of 660.'),
 ('III.2.9','III.3.7','The Baekje–Silla struggle over Han River territories belongs beside Jinheung’s expansion and the changing alliances of both courts.'),
 ('III.2.10','III.3.10','Baekje’s collapse and Silla’s expansion were linked through the same regional struggle, but they left distinct memories and successor communities.'),
 ('III.2.6','III.1.5','The loss of Hanseong is inseparable from Goguryeo’s Pyongyang-based southern strategy and its continuing contest for frontier access.'),
]
seen={frozenset((x['from'],x['to'])) for x in data['connections']}
for a,b,why in new_links:
 if frozenset((a,b)) in seen: continue
 data['connections'].append({'from':a,'to':b,'why':why})
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

a=R/'content/atlas/search-aliases.json';aliases=json.loads(a.read_text(encoding='utf-8'))
new_aliases={
 'III.2.1':['백제 4세기','한성백제','백제초기','Hanseong Baekje'],
 'III.2.2':['근초고왕','Geunchogo Baekje'],
 'III.2.3':['한성도읍','풍납토성','몽촌토성'],
 'III.2.4':['백제 남조 외교','양나라 백제 교류'],
 'III.2.5':['백제 왜 교류','백제 일본 교류'],
 'III.2.6':['한성함락','개로왕','웅진천도','475년 백제'],
 'III.2.7':['웅진백제','공산성','동성왕'],
 'III.2.8':['무령왕','무령왕릉','무령왕릉 지석','공주 무령왕릉'],
 'III.2.9':['사비천도','성왕','부여 사비','정림사지'],
 'III.2.10':['백제 멸망','의자왕','황산벌','660년','계백'],
}
for key,values in new_aliases.items():
 prior=aliases.get(key,[])
 aliases[key]=list(dict.fromkeys(prior+values))
a.write_text(json.dumps(aliases,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

f=R/'scripts/build_exploration.py';text=f.read_text(encoding='utf-8')
add=" ('baekje-river-maritime-complete','Baekje: the complete river and maritime kingdom','Ten connected studies follow the Han basin court, international exchange, the 475 catastrophe, Ungjin recovery, Sabi culture, and the fall of 660.','Ten connected readings',[f'III.2.{i}' for i in range(1,11)]),\n"
if 'baekje-river-maritime-complete' not in text:
 text=text.replace('trails=[]',add+'trails=[]') if False else text.replace(" ('ideas-and-expression'",add+" ('ideas-and-expression'")
 f.write_text(text,encoding='utf-8')
print('Batch I atlas',len(data['events']),'events',len(data['connections']),'connections; aliases',len(new_aliases))
