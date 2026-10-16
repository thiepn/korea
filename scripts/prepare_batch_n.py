#!/usr/bin/env python3
"""Curated Batch N Goryeo manuscripts: author-maintained Markdown -> deterministic replay-safe JSONL."""
from __future__ import annotations
import json,re,sys
from pathlib import Path
from build_corpus import WORD_RE,canonical
ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'content/imports/batch_n_goryeo.jsonl'
NEW_IDS={f'V.1.{i}' for i in (1,3,4,6,7,8,9,10)}
APPEND_IDS={'V.1.2','V.1.5'}
LONG_IDS={'V.1.1','V.1.4','V.1.7'}
SOURCES={
 'taejo':dict(institution='Academy of Korean Studies',title='태조 (Taejo of Goryeo)',url='https://encykorea.aks.ac.kr/Article/E0059032',role='Secondary historical reference; reign dates and royal strategy are contextual, not eyewitness testimony'),
 'goryeo':dict(institution='National Institute of Korean History',title='신편 한국사 12: 고려 왕조의 성립과 발전',url='https://contents.history.go.kr/front/nh/view.do?levelId=nh_012_0030_0010_0020_0050',role='Institutional synthesis of the early dynasty and its local political foundations'),
 'slaves':dict(institution='National Institute of Korean History',title='우리역사넷: 광종의 노비안검법과 고려사 사료',url='https://contents.history.go.kr/mobile/kc/view.do?code=kc_age_20&levelId=kc_i200500',role='Primary text excerpts and analysis; differentiates queen-biography portrayal and later criticism'),
 'adviser':dict(institution='National Institute of Korean History',title='최승로의 시무28조 — 사료로 본 한국사',url='https://contents.history.go.kr/mobile/hm/view.do?levelId=hm_046_0020',role='Primary-source transcription and historical introduction; surviving proposals are incomplete'),
 'memorial':dict(institution='Academy of Korean Studies',title='시무28조 (Twenty-Eight Proposals)',url='https://encykorea.aks.ac.kr/Article/E0032358',role='Authored scholarly interpretation; 982 submission and survival of 22 provisions'),
 'mok':dict(institution='National Institute of Korean History',title='성종의 12목 설치 — 사료로 본 한국사',url='https://contents.history.go.kr/mobile/hm/view.do?levelId=hm_046_0040',role='Primary Goryeosa text and commentary on Seongjong establishing twelve mok in 983'),
 'land':dict(institution='Academy of Korean Studies',title='전시과 — 한국민족문화대백과사전',url='https://encykorea.aks.ac.kr/Article/E0049507',role='Specialist scholarly article on initial land-revenue allotments in 976 and later revisions'),
 'granary':dict(institution='National Institute of Korean History',title='의창, 상평창, 대비원, 혜민국, 각종 보 — 사료로 본 한국사',url='https://contents.history.go.kr/front/hm/print.do?levelId=hm_063_0010&tabId=03&treeId=010403&whereStr=',role='Primary Goryeosa quotation and commentary on 993 sangpyeongchang provisions'),
}
SOURCE_KEYS={
'V.1.1':['taejo','goryeo'], 'V.1.3':['taejo','goryeo'],
'V.1.4':['slaves','adviser','memorial'], 'V.1.6':['land'],
'V.1.7':['memorial','mok','granary','adviser'], 'V.1.8':['goryeo'],
'V.1.9':['taejo','goryeo'], 'V.1.10':['mok','granary','land']}
# index is zero-based passage index; reference IDs are local to the article's sources list.
EVIDENCE={
'V.1.1':[(0,'Wang Geon ruled as Goryeo Taejo, whose reign ended in 943 and whose unification took effect after the Later Three Kingdoms struggles.','taejo','태조: 생애 및 주요 활동, 918–943','context'),(4,'National historical synthesis documents regional strongmen and the late-Silla power networks preceding Goryeo unification.','goryeo','Ⅰ. 고려 귀족사회의 형성 > 고려의 건국과 호족','context')],
'V.1.3':[(0,'Hyejong succeeded Taejo in 943 and Jeongjong followed amid succession uncertainty in the 940s.','goryeo','왕건 즉위 이후 초기 왕위 계승 및 정치적 혼란','context')],
'V.1.4':[(0,'Gwangjong ordered a review of servile status in 956, described in the later Goryeosa biography of Queen Daemok.','slaves','고려사 대목왕후 열전, 광종 7년 노비안검 조치','direct'),(3,'The civil service examination system began in Gwangjong’s reign and is part of the later debate about official selection.','memorial','시무28조: 오조정적평과 광종대 제도 변천','context'),(7,'Choe Seung-ro submitted an assessment of earlier rulers and political proposals to Seongjong in 982.','adviser','최승로 시무28조, 오조치적평과 현전 조항','direct')],
'V.1.6':[(0,'The initial jeonsigwa land-revenue allotment scheme was established in 976 under Gyeongjong.','land','전시과, 제정 시기와 시정전시과의 분급 기준','direct'),(2,'The land-allotment scheme distinguished revenue claims relating to agricultural and woodland resources.','land','전시과, 내용 / 전지 및 시지','direct')],
'V.1.7':[(0,'Choe Seung-ro presented proposals to Seongjong in 982; only 22 of the 28 clauses are extant.','memorial','시무28조: 982년 상서 / 28조 중 22조 전승','direct'),(2,'Seongjong established twelve mok in 983 to expand provincial administrative reach.','mok','고려사 권3, 성종 2년 2월 무자 / 12목 설치','direct'),(7,'The record of Seongjong’s 993 granary policy specifies stores at the two capitals and provincial centers.','granary','고려사 권80, 식화지 상평의창 성종 12년 2월','direct')],
'V.1.8':[(1,'The early Goryeo monarchy employed regional alliances and court-local institutions in integrating powerful provincial families.','goryeo','고려의 건국과 호족: 대호족정책, 호족의 동향','context')],
'V.1.9':[(0,'Taejo’s founding strategy connected Gaegyeong with northern political ambitions and later Seogyeong policy.','taejo','태조 주요 활동 / 북진 정책과 지방 관계','context')],
'V.1.10':[(1,'The 993 sangpyeongchang edict describes a grain stabilization scheme and its allocation across selected centers.','granary','고려사 권80, 성종 12년 2월 상평창','direct')],
}

def parse(path:Path)->dict[str,list[dict]]:
 text=path.read_text(encoding='utf-8')
 topics=list(re.finditer(r'(?m)^## (V\.1\.(?:10|[1-9]))\s*$',text));result={}
 for i,t in enumerate(topics):
  content=text[t.end():(topics[i+1].start() if i+1<len(topics) else len(text))]
  heads=list(re.finditer(r'(?m)^### (.+?)\s*$',content))
  blocks=[]
  for j,h in enumerate(heads):
   piece=content[h.end():(heads[j+1].start() if j+1<len(heads) else len(content))]
   paragraphs=[re.sub(r'\s+',' ',p).strip() for p in re.split(r'\n\s*\n',piece) if p.strip()]
   if not paragraphs or any(len(p)<90 for p in paragraphs):raise ValueError(f'Malformed authored passage {t[1]} / {h[1]}')
   blocks.append({'title':h[1].strip(),'paragraphs':paragraphs})
  if not blocks or t[1] in result:raise ValueError(f'Duplicate/empty canonical ID {t[1]}')
  result[t[1]]=blocks
 return result

def build():
 authored={**parse(ROOT/'content/editorial/batch_n_goryeo_deep.md'),**parse(ROOT/'content/editorial/batch_n_goryeo_short.md')}
 extensions=parse(ROOT/'content/editorial/batch_n_goryeo_append.md')
 if set(authored)!=NEW_IDS or set(extensions)!=APPEND_IDS:raise ValueError('Canonical coverage incomplete')
 known=canonical();rows=[];counts={};anchors=0
 for key,blocks in [*authored.items(),*extensions.items()]:
  if key not in known:raise ValueError('Unknown canonical ID '+key)
  count=sum(len(WORD_RE.findall(p)) for b in blocks for p in b['paragraphs']);counts[key]=count
  if key in LONG_IDS and count<2000:raise ValueError(f'Long essay below 2k {key}: {count}')
  if key in NEW_IDS-LONG_IDS and count<400:raise ValueError(f'Short subject below 400 {key}: {count}')
  if key in APPEND_IDS and count<180:raise ValueError(f'Append-only essay below 180 {key}: {count}')
  sources=SOURCE_KEYS.get(key,[])
  record={'id':key,'mode':'replace' if key in NEW_IDS else 'append','blocks':blocks}
  if key in NEW_IDS:
   record.update(release='N',kicker='EARLY GORYEO · TENTH-CENTURY STATE FORMATION',description='Original historical account of governing, reform and society in early Goryeo.',sourceStatus='Original editorial synthesis with selected Korean-language primary-text anchors and secondary research; later compilations are distinguished from tenth-century testimony.',sources=[SOURCES[k] for k in sources])
   for bi,claim,source,locator,kind in EVIDENCE.get(key,[]):
    if bi>=len(blocks):raise ValueError(f'Missing evidence passage {key}:{bi}')
    blocks[bi].setdefault('evidence',[]).append({'claim':claim,'sourceIndex':sources.index(source),'locator':locator,'type':kind});anchors+=1
  rows.append(record)
 raw=''.join(json.dumps(r,ensure_ascii=False,separators=(',',':'))+'\n' for r in rows)
 OUTPUT.parent.mkdir(parents=True,exist_ok=True)
 if not OUTPUT.exists() or OUTPUT.read_text(encoding='utf-8')!=raw:OUTPUT.write_text(raw,encoding='utf-8')
 return {'new_articles':len(authored),'deepened_articles':len(extensions),'new_passages':sum(len(x['blocks']) for x in rows),'authored_words':sum(counts.values()),'evidence_anchors':anchors,'words_by_article':counts}
if __name__=='__main__':
 try:print(json.dumps(build(),ensure_ascii=False,indent=2))
 except Exception as exc:print('FAILED',exc,file=sys.stderr);raise SystemExit(1)
