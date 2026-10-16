#!/usr/bin/env python3
"""Integrate later-Joseon family history into the existing atlas and reading paths."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
P=R/'content/atlas/atlas.json';A=R/'content/atlas/search-aliases.json';E=R/'scripts/build_exploration.py'
def build():
 atlas=json.loads(P.read_text(encoding='utf8'))
 events=[
  (1600,'VII.5.1','Seventeenth–eighteenth centuries','Lineage compilations shift toward paternal succession','The organization of printed genealogies increasingly emphasizes male-line descendants; the transition varies by family and surviving edition.'),
  (1650,'VII.5.4','Later Joseon','Childhood depends on a web of labor and care','Household instructions, inheritance papers and informal teaching reveal different demands on children across social ranks.'),
  (1680,'VII.5.5','Later Joseon','Household work sustains family status','Domestic production and service connect food, textile making, household management and unequal labor obligations.'),
  (1700,'VII.5.6','Seventeenth–nineteenth centuries','Inner and outer quarters become increasingly differentiated','In substantial houses, the changing anchae and sarangchae layout registers gendered reception, work and ritual space.'),
  (1720,'VII.5.7','Later Joseon','Food preservation and consumption show regional contrasts','Household diet follows local crops, price shocks, seasonal preservation, labor and uneven access to resources.'),
  (1740,'VII.5.8','Later Joseon','Clothing displays rank and transforms through fashion','Materials, labor, conventions and market availability affect dress and the visual negotiation of status.'),
  (1760,'VII.5.9','Later Joseon','Medical care combines formal institutions and household support','Female practitioners, medical examinations and kin caregiving operated within unequal systems of access.'),
  (1800,'VII.5.10','Later Joseon','Mourning and ritual succession reorder family obligations','The conduct of funerals and lineage remembrance combines formal ritual ideals with costs, care and local variation.'),
 ]
 keys={(e['year'],e['id']) for e in atlas['events']}
 for year,id,date,title,detail in events:
  if (year,id) not in keys:atlas['events'].append({'year':year,'id':id,'era':'VII','date':date,'title':title,'detail':detail})
 atlas['events'].sort(key=lambda e:e['year'])
 links=[
  ('VII.5.1','VII.5.2','The genealogical claim of paternal succession shaped, but never fully determined, marriage and residence decisions.'),
  ('VII.5.1','VII.5.3','Women sometimes managed property and labor despite declining prominence in male-line genealogical representations.'),
  ('VII.5.1','VII.5.10','Ritual succession and ancestry books give related but different accounts of who should sustain family memory.'),
  ('VII.5.2','VII.5.4','Marriage arrangements shaped where children lived, who supported their education and which relatives contributed to care.'),
  ('VII.5.3','VII.5.5','Women’s practical authority becomes visible through household stores, textile work and the supervision of dependent labor.'),
  ('VII.5.4','VII.5.9','Birth, childhood illness and adult care relied upon overlapping household and specialist networks.'),
  ('VII.5.5','VII.5.6','The kitchen, courtyard and inner quarters were workplaces, not simply picturesque architectural features.'),
  ('VII.5.5','VII.5.7','Food preservation exposes the hidden time, fuel and labor underpinning hospitality and daily meals.'),
  ('VII.5.6','VII.5.8','Dress and residential layout each marked hierarchy, but material resources limited what ideals could be realized.'),
  ('VII.5.7','VII.5.9','Diet, scarcity and household reserves affected both vulnerability to disease and the resources available for care.'),
  ('VII.5.9','VII.5.10','Serious illness and deaths could turn medical decisions into mourning, succession and economic survival problems.'),
  ('VII.5.1','VI.4.3','Changes in Korean writing expanded some forms of household communication without eliminating the prestige of classical genealogies.'),
  ('VII.5.5','IV.3.6','Specialized craft labor in Silla offers a longer perspective on production without treating the two periods as identical.'),
  ('VII.5.7','VIII.1.10','The everyday consequences of nineteenth-century opening can be compared with earlier household food networks and regional prices.'),
  ('VII.5.4','X.3.1','Education in later Joseon illustrates how the meanings of literacy, opportunity and family investment changed historically.'),
  ('VII.5.9','X.4.3','Later medical institutions and household care invite comparison with modern health systems while avoiding anachronistic diagnosis.'),
 ]
 pairs={frozenset((c['from'],c['to'])) for c in atlas['connections']}
 for f,t,why in links:
  k=frozenset((f,t))
  if k not in pairs:atlas['connections'].append({'from':f,'to':t,'why':why});pairs.add(k)
 P.write_text(json.dumps(atlas,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 alias=json.loads(A.read_text(encoding='utf8'))
 values={
 'VII.5.1':['족보','문중','종법','부계친족'],
 'VII.5.2':['혼인','거주','분재기','상속'],
 'VII.5.3':['조선 여성 재산','여성 노동','여성 권한'],
 'VII.5.4':['조선 육아','서당','아동 교육','어린이'],
 'VII.5.5':['가사노동','노비','가내 생산','생계'],
 'VII.5.6':['안채','사랑채','온돌','조선 한옥'],
 'VII.5.7':['조선 음식','식생활','담배','음식 저장'],
 'VII.5.8':['조선 복식','저고리','의복','신분 표시'],
 'VII.5.9':['의녀','혜민서','의과','조선 질병'],
 'VII.5.10':['상례','제사','삼년상','장례'],
 }
 for k,terms in values.items():alias[k]=list(dict.fromkeys(alias.get(k,[])+terms))
 A.write_text(json.dumps(alias,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 src=E.read_text(encoding='utf8')
 if 'late-joseon-family-complete' not in src:
  anchor=" ('ideas-and-expression','Ideas and expression'"
  line=" ('late-joseon-family-complete','Later Joseon: families and everyday life','Ten connected studies of lineages, marriage, childhood, labor, houses, clothing, food, illness and mourning in a changing society.','Ten connected readings',[f'VII.5.{i}' for i in range(1,11)]),\n"
  if anchor not in src:raise ValueError('Route anchor missing')
  E.write_text(src.replace(anchor,line+anchor),encoding='utf8')
 return {'events':len(atlas['events']),'connections':len(atlas['connections']),'aliasSubjects':len(alias)}
if __name__=='__main__':print(json.dumps(build(),indent=2))
