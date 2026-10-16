#!/usr/bin/env python3
"""Add only curated and validated opening-era discovery data."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
ATL=ROOT/'content/atlas/atlas.json';A=ROOT/'content/atlas/search-aliases.json'; E=ROOT/'scripts/build_exploration.py'

def build():
 atlas=json.loads(ATL.read_text(encoding='utf8'))
 events=[
  (1876,'VIII.1.3','1876–1882','Foreign merchants encounter a changing jurisdiction','Extraterritorial rules and new commercial settlement arrangements altered how disputes could be heard, creating uneven legal protection around early treaty ports.'),
  (1876,'VIII.1.4','1876 onward','Trade routes begin to shift toward external buyers','After the first commercial arrangements, Korean grain routes increasingly connected inland suppliers with foreign vessels, amid harvest uncertainty and tariff controversy.'),
  (1880,'VIII.1.2','1880','Wonsan joins the treaty-port network','Wonsan opened in 1880 after Busan had begun its new phase of foreign trade, drawing local transporters and merchants into an unevenly regulated coastal economy.'),
  (1880,'VIII.1.7','1880–1881','Joseon chaekryak provokes a strategic controversy','Kim Hong-jip brought Huang Zunxian’s policy text to court after his 1880 Japan mission; its proposals prompted disagreement over opening, alliances and state legitimacy.'),
  (1880,'VIII.1.8','1880–1882','Qing mediation shapes Korea’s new diplomatic choices','Qing China, Japan, and the prospect of links with the United States figured in Joseon debates about external pressure, administrative reform and political autonomy.'),
  (1881,'VIII.1.6','1881','Yeongseonsa learners depart for Qing technical training','Kim Yun-sik led trainees toward Tianjin arsenals and discussions with Qing officials, combining military technology education and wider diplomatic consultation.'),
  (1882,'VIII.1.9','22 May 1882','Joseon and the United States sign a treaty','At Jemulpo, Korean and American plenipotentiaries signed an agreement combining friendship clauses, consular arrangements and commercial provisions.'),
  (1882,'VIII.1.10','1876–1882','Early opening changes local economies and knowledge','Across port towns and inland networks, new patterns of grain trade, technical education, foreign residence and official authority affected communities unevenly.'),
 ]
 base={(x['year'],x['id']) for x in atlas['events']}
 for year,key,date,title,detail in events:
  if (year,key) not in base:atlas['events'].append({'year':year,'id':key,'era':'VIII','date':date,'title':title,'detail':detail})
 atlas['events'].sort(key=lambda x:x['year'])
 links=[
  ('VIII.1.1','VIII.1.3','The treaty’s legal provisions acquire practical meaning in the unequal judicial rules governing Japanese merchants and their disputes with Korean traders.'),
  ('VIII.1.2','VIII.1.4','Coastal ports and inland grain routes form one economic system: shipping changes alter what wholesalers and producers can sell and where.'),
  ('VIII.1.3','VIII.1.9','Comparing treaty-based legal privileges in the Japanese port regime and the later American agreement clarifies why particular clauses matter.'),
  ('VIII.1.4','IV.3.7','Early treaty-port commerce can be compared with Silla markets to show continuity in Korean brokerage and differences in foreign legal structures.'),
  ('VIII.1.5','VIII.1.7','Reports gathered in Meiji Japan entered Korean debates about reform, including which foreign practices could be learned without political dependence.'),
  ('VIII.1.6','VIII.1.9','The Tianjin mission combined military-technical training with consultations relevant to the diplomatic route toward the 1882 United States treaty.'),
  ('VIII.1.7','VI.4.3','Arguments over translation and institutional learning echo earlier choices about language, authority and the politics of writing in Joseon.'),
  ('VIII.1.8','VIII.1.9','The American treaty followed a wider debate about balancing neighboring powers and the limits of assurances made in an unequal strategic setting.'),
  ('VIII.1.10','VII.6.5','To understand opening-era trade, compare earlier Joseon market institutions and the changing pressures placed on local producers and carriers.'),
  ('VIII.1.3','IX.1.6','Different foreign jurisdictions and later occupation administration can be compared without assuming they were legally identical systems.'),
  ('VIII.1.4','X.2.4','Economic adjustment in treaty-port households offers a longer perspective on how external markets reshape work and distribute risks unevenly.'),
  ('VIII.1.6','IV.3.6','Technical artisans in the Tianjin mission provide a contrast with earlier specialized craft labor and the changing social value of practical knowledge.'),
  ('VIII.1.7','VIII.9.2','The disagreements over opening form a necessary earlier context for the later variety of nationalist and reformist programs under colonial pressure.'),
  ('VIII.1.9','IX.1.10','Hopes attached to foreign friendship clauses can be read beside the much later limits of external support during Korea’s division and diplomacy.'),
  ('VIII.1.10','X.3.1','The uneven household effects of economic opening invite comparison with later debates about education, social opportunity and economic inequality.'),
  ('VIII.1.2','III.2.2','Comparing Baekje maritime exchange with nineteenth-century treaty ports shows that foreign contact predates the treaty system by many centuries.'),
 ]
 pairs={frozenset((c['from'],c['to'])) for c in atlas['connections']}
 for a,b,why in links:
  pair=frozenset((a,b))
  if pair not in pairs:atlas['connections'].append({'from':a,'to':b,'why':why});pairs.add(pair)
 ATL.write_text(json.dumps(atlas,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 aliases=json.loads(A.read_text(encoding='utf8'))
 additional={
 'VIII.1.1':['강화도 조약','조일수호조규','불평등조약'],
 'VIII.1.2':['부산 개항','원산 개항','개항장'],
 'VIII.1.3':['일본상인','치외법권','영사재판권'],
 'VIII.1.4':['개항 무역','미곡 수출','관세','개항기 통상'],
 'VIII.1.5':['수신사','김홍집','메이지 일본'],
 'VIII.1.6':['영선사','김윤식','톈진기기국'],
 'VIII.1.7':['개화파','조선책략','위정척사','영남만인소'],
 'VIII.1.8':['청나라 외교','황준헌','연미론'],
 'VIII.1.9':['조미수호통상조약','신헌','슈펠트','거중조정'],
 'VIII.1.10':['개항기 사회','개항과 생활','대외교류'],
 }
 for key,terms in additional.items():
  old=aliases.get(key,[]);aliases[key]=list(dict.fromkeys(old+terms))
 A.write_text(json.dumps(aliases,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 text=E.read_text(encoding='utf8')
 needle=" ('ideas-and-expression','Ideas and expression'"
 title=" ('opening-korea-treaty-ports-complete','Opening Korea: the full treaty-port Chapter','Ten connected histories of commerce, jurisdiction, Qing and Japanese diplomacy, technical learning, ideas, and the 1882 United States treaty.','Ten connected readings',[f'VIII.1.{i}' for i in range(1,11)]),\n"
 if "opening-korea-treaty-ports-complete" not in text:
  if needle not in text:raise ValueError('Route insertion anchor changed')
  E.write_text(text.replace(needle,title+needle),encoding='utf8')
 return {'events':len(atlas['events']),'connections':len(atlas['connections']),'aliases':len(aliases)}
if __name__=='__main__':print(json.dumps(build(),indent=2))
