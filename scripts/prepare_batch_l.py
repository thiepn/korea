#!/usr/bin/env python3
"""Batch L: original opening-period manuscripts, replay-safe import and accountable sources."""
from __future__ import annotations
import json,re,sys
from pathlib import Path
from prepare_batch_j import parse
from build_corpus import canonical,WORD_RE
R=Path(__file__).resolve().parents[1]
OUTPUT=R/'content/imports/batch_l_treaty_ports.jsonl'
REF={
 'us_treaty':dict(institution='National Institute of Korean History',title='조미 수호 통상 조약 — 1882 source transcription / Original Chinese Text of Treaty',url='https://contents.history.go.kr/mobile/hm/view.do?levelId=hm_115_0060',role='Primary Chinese-language treaty text, dated 22 May 1882, including named signatories, friendship clause and consular provisions'),
 'us_history':dict(institution='National Institute of Korean History',title='우리역사넷 — 조미 수호 통상 조약 및 대외 관계',url='https://contents.history.go.kr/mobile/ta/view.do?levelId=ta_h42_0040_0010_0020',role='Secondary account of negotiation context and treaty characteristics, not an independent guarantee of later intervention'),
 'rice':dict(institution='National Institute of Korean History',title='한국문화사 26 — 개항과 쌀 수출',url='https://contents.history.go.kr/mobile/km/view.do?levelId=km_026_0060_0010_0010_0010',role='Source-backed history of 1876 scarcity, Busan grain exports, Wonsan and Incheon opening dates'),
 'rice_routes':dict(institution='National Institute of Korean History',title='한국문화사 26 — 쌀 수출의 증가와 유통권',url='https://contents.history.go.kr/mobile/km/view.do?levelId=km_026_0060_0010_0010_0020',role='Documented regional grain circuits and changing internal distribution before and after 1876'),
 'susinsa':dict(institution='Academy of Korean Studies',title='수신사 — 한국민족문화대백과사전',url='https://encykorea.aks.ac.kr/Article/E0031506',role='Scholarly account of 1876, 1880 and 1881 Japan missions and customs negotiation'),
 'yeongseonsa':dict(institution='Academy of Korean Studies',title='영선사 — 한국민족문화대백과사전',url='https://encykorea.aks.ac.kr/Article/E0037460',role='Institutional history of 1881 Tianjin technical learners, mission interruption and treaty mediation; participant counts distinguish categories'),
 'diplomatic_docs':dict(institution='Academy of Korean Studies',title='계하자문책 — Korean diplomatic communications of 1881–1882',url='https://encykorea.aks.ac.kr/Article/E0003270',role='Catalog and historical description of contemporary compiled diplomatic correspondence sent to Qing offices'),
 'tianjin_notes':dict(institution='Academy of Korean Studies',title='천진담초 — 김윤식 diplomatic talks in Tianjin',url='https://encykorea.aks.ac.kr/Article/E0056056',role='Description of Kim Yun-sik meeting record, a primary documentary witness to Qing-linked negotiations'),
 'joseon_chaekryak':dict(institution='Academy of Korean Studies',title='조선책략 — 한국민족문화대백과사전',url='https://encykorea.aks.ac.kr/Article/E0052228',role='Huang Zunxian pamphlet and 1880 circulation; policy perspective and subsequent opposition'),
 'petition':dict(institution='Academy of Korean Studies',title='홍시중 — reference to 1881 영남만인소',url='https://encykorea.aks.ac.kr/Article/E0064229',role='Historical contextual source for 1881 petition campaign against the reform policy'),
 'office':dict(institution='Academy of Korean Studies',title='통리기무아문 관제 — 한국민족문화대백과사전',url='https://encykorea.aks.ac.kr/Article/E0005000',role='Source-based institutional chronology for opening-period reorganization of specialized government offices'),
 'trade_office':dict(institution='Academy of Korean Studies',title='통상사 — 한국민족문화대백과사전',url='https://encykorea.aks.ac.kr/Article/E0059338',role='Opening-period office handling foreign commerce and the changes after 1882'),
}
SOURCES={
 'VIII.1.3':['susinsa','rice_routes','us_treaty','trade_office'],
 'VIII.1.4':['rice','rice_routes','susinsa'],
 'VIII.1.6':['yeongseonsa','tianjin_notes','diplomatic_docs'],
 'VIII.1.7':['joseon_chaekryak','petition','office','susinsa'],
 'VIII.1.8':['joseon_chaekryak','us_history','diplomatic_docs','office'],
 'VIII.1.9':['us_treaty','us_history','tianjin_notes','diplomatic_docs'],
 'VIII.1.10':['rice','rice_routes','trade_office'],
}
# index (zero-based), claim, source, precise locator, type; do not treat policy arguments as empirical truths.
CLAIMS={
 'VIII.1.3':[(1,'Treaty arrangements created consular judicial privileges affecting jurisdiction involving foreign nationals.','us_treaty','Articles on consular jurisdiction; direct text concerns the 1882 United States treaty as a comparative instrument','context'),(7,'Regional Korean merchants and coastal shipping predated the nineteenth-century opening of ports.','rice_routes','개항과 쌀 수출, discussion of West and East Sea trade circuits','context')],
 'VIII.1.4':[(1,'A Korean harvest shortage in 1876 produced a temporary influx of Japanese rice before later export growth.','rice','개항과 쌀 수출, early grain-trade paragraph','direct'),(3,'The pre-existing grain distribution routes connected southern Korea, Dongnae, and Wonsan.','rice_routes','쌀 수출의 증가와 유통권, first section','direct')],
 'VIII.1.6':[(0,'Kim Yun-sik led the 1881 Yeongseonsa training delegation toward Qing military and technical education.','yeongseonsa','영선사, contents and dispatch','direct'),(1,'Institutional accounts distinguish the mission party from trainee and artisan counts.','yeongseonsa','영선사, trainees and composition; compare category definitions','context'),(3,'The Tianjin mission had a role in talks related to the impending 1882 Korea–United States treaty.','tianjin_notes','천진담초, recorded meeting purposes','direct'),(4,'The 1882 Imo crisis curtailed the mission training program.','yeongseonsa','영선사, disruption and return','direct')],
 'VIII.1.7':[(2,'Kim Hong-jip brought Huang Zunxian’s Joseon chaekryak into Korean discussion after the 1880 mission.','joseon_chaekryak','조선책략, 편찬/발간 경위','direct'),(3,'The 1881 Yeongnam collective petition expressed organized criticism of opening policy.','petition','홍시중, 영남만인소 paragraph','context'),(6,'The Tongni Gimu Amun was organized with specialized bureaus in late 1880 and restructured afterward.','office','관제, initial twelve offices and 1881 reorganization','context')],
 'VIII.1.8':[(2,'Joseon chaekryak recommended Qing, Japanese, and United States ties against perceived Russian danger.','joseon_chaekryak','조선책략, content and strategic argument','direct'),(3,'The Tongni Gimu Amun reorganized trade, diplomatic, military and technological tasks.','office','관제, initial specialized sections','context')],
 'VIII.1.9':[(0,'The Korea–United States treaty was signed on 22 May 1882.','us_treaty','Primary treaty heading and signatures, May 22, 1882','direct'),(1,'Korean plenipotentiaries Sin Heon and Kim Hong-jip and United States representative Shufeldt appear in the treaty.','us_treaty','Preamble naming signatories','direct'),(2,'Article One uses language of assistance and friendly offices when another country acts unjustly.','us_treaty','第一款, original Chinese primary text','direct'),(4,'The treaty contains clauses dealing with diplomatic residence and consular arrangements.','us_treaty','第二款 and subsequent clauses','direct'),(6,'Qing officials participated in the diplomacy leading to the 1882 treaty.','tianjin_notes','천진담초, 1881 treaty preliminary discussions','context')],
 'VIII.1.10':[(1,'Rice export routes redirected southern Korean grain toward Busan and Japan after opening.','rice_routes','쌀 수출의 증가와 유통권, market distribution section','context')],
}
def parse_append(path):
 s=path.read_text(encoding='utf8');parts=re.split(r'(?m)^## (VIII\.1\.\d+)\s*$',s);out={}
 for i in range(1,len(parts),2):
  key,body=parts[i],parts[i+1];chunks=re.split(r'(?m)^### (.+?)\s*$',body);blocks=[]
  for j in range(1,len(chunks),2):
   content=chunks[j+1].strip()
   if len(content)<120:raise ValueError('Too short append '+key)
   blocks.append({'title':chunks[j],'paragraphs':[content]})
  if not blocks:raise ValueError('Missing append for '+key)
  out[key]=blocks
 return out

def records():
 deep=parse(R/'content/editorial/batch_l_treaty_ports_deep.md')
 short=parse(R/'content/editorial/batch_l_treaty_ports_collections.md')
 append=parse_append(R/'content/editorial/batch_l_treaty_ports_deepening.md')
 expected={f'VIII.1.{i}' for i in (3,4,6,7,8,9,10)}
 if set(deep)|set(short)!=expected or set(deep)&set(short) or set(append)!={'VIII.1.1','VIII.1.2','VIII.1.5'}:raise ValueError('Canonical VIII.1 source mismatch')
 long_ids={'VIII.1.3','VIII.1.7','VIII.1.9'}
 if set(deep)!=long_ids:raise ValueError('Expected three deep essays')
 allowed=canonical();rows=[];counts={};anchors=0
 for key,blocks in [*deep.items(),*short.items(),*append.items()]:
  if key not in allowed:raise ValueError('Unknown canonical ID '+key)
  count=sum(len(WORD_RE.findall(p)) for b in blocks for p in b['paragraphs']);counts[key]=count
  if key in long_ids and count<2000:raise ValueError('Less than 2000 words '+key+': '+str(count))
  if key in short and count<550:raise ValueError('Shorter subject not adequately treated '+key)
  if key in append and count<110:raise ValueError('Append too short '+key)
  record={'id':key,'mode':'replace' if key in expected else 'append','blocks':blocks}
  if key in expected:
   refs=SOURCES[key];record.update(release='L',kicker='THE TREATY-PORT WORLD · LATE JOSEON',description='An original historical account of changing law, commerce, diplomacy, technical learning, and daily life after the opening.',sourceStatus='Selective primary-text and institutional contextual annotations; historical synthesis has not been independently reviewed claim by claim.',sources=[REF[x] for x in refs])
   for index,claim,source,locator,kind in CLAIMS.get(key,[]):
    if index>=len(blocks):raise ValueError(f'Evidence index out of bounds {key}:{index}')
    blocks[index].setdefault('evidence',[]).append({'claim':claim,'sourceIndex':refs.index(source),'locator':locator,'type':kind});anchors+=1
  rows.append(record)
 return rows,dict(new_articles=len(expected),deepened_articles=len(append),new_passages=sum(len(r['blocks']) for r in rows),authored_words=sum(counts.values()),anchors=anchors,counts=counts)

def build():
 rows,metrics=records();blob=''.join(json.dumps(r,ensure_ascii=False,separators=(',',':'))+'\n' for r in rows)
 OUTPUT.parent.mkdir(parents=True,exist_ok=True)
 if not OUTPUT.exists() or OUTPUT.read_text(encoding='utf8')!=blob:OUTPUT.write_text(blob,encoding='utf8')
 return metrics
if __name__=='__main__':
 try:print(json.dumps(build(),ensure_ascii=False,indent=2))
 except Exception as ex:print('Batch L rejected:',ex,file=sys.stderr);sys.exit(1)
