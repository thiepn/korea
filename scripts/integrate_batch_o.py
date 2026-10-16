#!/usr/bin/env python3
"""Extend established explorer without changing historical source IDs or reader code."""
from __future__ import annotations
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
AT=R/'content/atlas/atlas.json';AL=R/'content/atlas/search-aliases.json';RO=R/'scripts/build_exploration.py'
EVENTS=[
 (1000,'Goryeo dynasty, broad historical theme','V.5.10','Religious life beyond royal monuments','Everyday donations, seasonal rites and community institutions are incompletely represented by court chronicles.'),
 (918,'918','V.5.1','Palgwan rite appears at the new Goryeo court','The later Goryeosa record of Taejo’s first year recalls a Palgwan ritual continuing earlier precedent.'),
 (1010,'1010','V.5.7','Yeondeunhoe revived under Hyeonjong','A later ritual record dates the restored court lantern ceremony to Hyeonjong’s first year.'),
 (1085,'1085–1086','V.5.3','Uicheon studies Buddhist scholarship in Song','Accounts of the royal monk’s travels and return show Goryeo’s participation in transregional textual networks.'),
 (1097,'1097','V.5.3','Uicheon assumes the Gukcheongsa abbacy','The completion of the temple and Uicheon’s lectures provided an institutional home for Cheontae learning.'),
 (1236,'1236 onward','V.5.6','Re-carving the Buddhist canon during Mongol warfare','The state-backed re-engraving program responded to disaster and supported major scholarly and ritual labor.'),
 (1910,'After 1910','VIII.9.1','Underground and exile independence networks expand','The loss of Korean sovereignty gave disparate organizations new and dangerous coordination problems.'),
 (1919,'1 March 1919','VIII.9.2','March First independence declaration and protests','Participants circulated an independence declaration and organized protests under colonial repression.'),
 (1919,'11 April 1919','VIII.9.3','Provisional Charter proclaims a democratic republic','The Shanghai provisional government’s charter asserts republican authority and formal equality.'),
 (1920,'June 1920','VIII.9.4','Korean armed units fight at Bongodong','The battle became a significant episode of armed resistance beyond the peninsula.'),
 (1923,'1923','VIII.9.3','National Representatives’ Conference debates movement reform','Activists debated legitimacy, representation and reorganization of the provisional institutions.'),
 (1926,'10 June 1926','VIII.9.8','Students stage the June Tenth demonstrations','Public events around Sunjong’s funeral became the occasion for organized independence protest.'),
 (1927,'February 1927','VIII.9.9','Singanhoe unites nationalist and socialist organizers','The association formed a cross-ideological front under colonial constraints.'),
 (1929,'November 1929 onward','VIII.9.8','Gwangju student protest spreads','School grievances and anticolonial mobilization intersected as demonstrations extended beyond Gwangju.'),
 (1931,'After 1931','VIII.9.10','Independence strategies adapt to Japan’s expansion in China','The Manchurian crisis changed alliances, risks and possibilities for Korean groups operating abroad.'),
]
CONNECTIONS=[
 ('V.5.1','V.1.1','Goryeo kingship depended on legitimating rituals as well as the settlement of provincial political loyalties.'),
 ('V.5.1','V.5.7','Royal sponsorship and lay religious participation shared ceremonial forms without carrying the same social obligations.'),
 ('V.5.2','V.5.3','Uicheon’s scholarship makes sense within older doctrinal and meditative networks, not as a solitary invention.'),
 ('V.5.3','V.5.6','Collecting and interpreting commentaries complements, but should not be conflated with, different state Buddhist canon projects.'),
 ('V.5.3','V.5.4','Uicheon’s synthetic program and Jinul’s reform occupied overlapping but distinct institutional and chronological settings.'),
 ('V.5.5','V.5.10','Temple endowments and labor claims reveal the unequal material conditions of lay religious life.'),
 ('V.5.7','IV.3.8','Ceremonial consumption and urban craft production illuminate connections between material culture and sacred display.'),
 ('V.5.8','V.1.7','Confucian moral government and Buddhist patronage coexisted within debates about institutional authority.'),
 ('V.5.9','II.1.8','Historical memory of local sacred landscapes changed over centuries, without implying unchanged cults from antiquity.'),
 ('VIII.9.1','VIII.9.2','Clandestine organizing and public protest answered different problems under colonial repression.'),
 ('VIII.9.2','VIII.9.3','Mass protest helped make republican independence a claim requiring concrete institutions.'),
 ('VIII.9.3','VIII.9.4','Government-in-exile diplomacy and borderland armed resistance followed intersecting, sometimes competing paths.'),
 ('VIII.9.3','IX.1.1','The language of 1919 republican legitimacy was remembered and contested again amid liberation in 1945.'),
 ('VIII.9.4','VIII.9.10','Borderland campaigns in 1920 and later armed units operated under changing regional political pressures.'),
 ('VIII.9.5','VIII.9.6','Direct-action activists and gradualist cultural organizers disagreed over methods but both reacted to colonial power.'),
 ('VIII.9.7','VIII.9.9','Class-based movements and the Singanhoe united-front experiment overlapped without erasing ideological differences.'),
 ('VIII.9.8','VIII.9.9','Student activism and the united front created channels for broader public organizing.'),
 ('VIII.9.8','VI.4.3','School-based activism highlights how literacy and institutions could carry political ideas far beyond earlier royal writing reforms.'),
 ('VIII.9.10','IX.3.3','Armed organization in the Chinese theater precedes a different set of military and civilian experiences during the Korean War.'),
 ('V.5.10','VII.5.3','Religious activity and gendered household life are connected across periods but require separate source criticism.'),
]
ALIASES={
 'V.5.1':['고려 호국불교','불교 왕권','팔관회'],'V.5.2':['교종','선종','고려 교단'],'V.5.3':['의천','대각국사','천태종','교장','국청사'],
 'V.5.4':['지눌','수선사','조계종'],'V.5.5':['사원 경제','사찰 토지','고려 사찰'],'V.5.6':['고려대장경','팔만대장경','교장도감'],
 'V.5.7':['연등회','팔관회','고려 불교 의례'],'V.5.8':['고려 유교','국자감','조상 제사'],'V.5.9':['풍수','도교','고려 민간신앙'],
 'V.5.10':['고려 여성 신앙','재가 신도','일상 종교'],'VIII.9.1':['국외 독립운동','간도','연해주 독립운동'],
 'VIII.9.2':['삼일운동','3.1운동','독립선언서'],'VIII.9.3':['대한민국 임시정부','임시헌장','상하이 임정','국민대표회의'],
 'VIII.9.4':['봉오동 전투','청산리 전투','홍범도','김좌진'],'VIII.9.5':['의열단','김원봉','무장 독립운동'],
 'VIII.9.6':['실력양성운동','민립대학','문화민족주의'],'VIII.9.7':['사회주의 운동','노동 운동','소작 쟁의'],
 'VIII.9.8':['육십만세운동','6.10만세운동','광주학생항일운동','광주학생운동'],'VIII.9.9':['신간회','민족협동전선'],
 'VIII.9.10':['한국광복군','중국 관내 독립운동','1930년대 무장투쟁'],
}
def build():
 atlas=json.loads(AT.read_text(encoding='utf8'))
 atlas['events']=[event for event in atlas['events'] if not (event['id']=='V.5.10' and event['year']==-1)]
 event_keys={(e['id'],e['year']) for e in atlas['events']}
 for year,date,key,title,detail in EVENTS:
  if (key,year) not in event_keys:
   atlas['events'].append({'date':date,'year':year,'era':key.split('.')[0],'id':key,'title':title,'detail':detail});event_keys.add((key,year))
 connection_keys={frozenset((e['from'],e['to'])) for e in atlas['connections']}
 for source,dest,why in CONNECTIONS:
  k=frozenset((source,dest))
  if k not in connection_keys:atlas['connections'].append({'from':source,'to':dest,'why':why});connection_keys.add(k)
 atlas['events'].sort(key=lambda event:(event['year'],event['id']))
 AT.write_text(json.dumps(atlas,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 aliases=json.loads(AL.read_text(encoding='utf8'))
 for key,terms in ALIASES.items():aliases[key]=list(dict.fromkeys(aliases.get(key,[])+terms))
 AL.write_text(json.dumps(aliases,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 s=RO.read_text(encoding='utf8')
 for anchor,line in [('goryeo-religion-complete'," ('goryeo-religion-complete','Goryeo: religion and the many worlds of belief','Ten linked histories of kingship, monastic work, learning, rites, lay devotion, and the meeting of Buddhist and Confucian practice.','Ten connected readings',[f'V.5.{i}' for i in range(1,11)]),\n"),('independence-movements-complete'," ('independence-movements-complete','Korean independence: movements and contested strategies','Ten linked histories of 1919 republicanism, borderland armed movements, cultural and class politics, students, and wartime resistance.','Ten connected readings',[f'VIII.9.{i}' for i in range(1,11)]),\n")]:
  if anchor not in s:
   target=" ('ideas-and-expression','Ideas and expression'"
   if target not in s:raise ValueError('Missing route insert point')
   s=s.replace(target,line+target)
 RO.write_text(s,encoding='utf8')
 return {'events':len(atlas['events']),'connections':len(atlas['connections']),'aliasSubjects':len(aliases)}
if __name__=='__main__':print(json.dumps(build(),indent=2))
