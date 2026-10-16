#!/usr/bin/env python3
"""Batch J original social-history manuscript to idempotent canonical JSONL events.

Source provenance is deliberately selective: direct primary texts versus modern contextual
interpretations, never a claim that the entire manuscript has undergone peer review.
"""
from __future__ import annotations
import json,re,sys
from pathlib import Path
from build_corpus import DATA,canonical,WORD_RE
R=Path(__file__).resolve().parents[1]
OUTPUT=R/'content/imports/batch_j_silla_society.jsonl'
REFS={
 'village_primary':dict(institution='National Institute of Korean History',title='신라의 촌락 지배 — text and commentary on the Silla Village Register',url='https://contents.history.go.kr/front/hm/print.do?levelId=hm_033_0050&tabId=03&treeId=010302&whereStr=',role='Published transcription of the primary village register; household, slave, field, livestock and tree entries; document dating debated'),
 'village_analysis':dict(institution='National Institute of Korean History',title='신라촌락문서 — historical chronology and document survival',url='https://contents.history.go.kr/mobile/kc/view.do?code=kc_age_10&levelId=kc_r100485',role='Secondary synthesis for provenance, discovery and document scope'),
 'village_critical':dict(institution='Academy of Korean Studies',title='신라 촌락문서',url='https://encykorea.aks.ac.kr/Article/E0032861',role='Scholarly encyclopedia discussion of fragmentary preservation and competing datings'),
 'land_analysis':dict(institution='National Institute of Korean History',title='신편 한국사 — 통일 신라의 수취제도',url='https://contents.history.go.kr/front/nh/view.do?levelId=nh_001_0040_0020_0020_0010',role='Scholarly interpretation of household grades, taxation and land categories; disputed institutional meanings'),
 'field_table':dict(institution='National Institute of Korean History',title='한국문화사 — 신라 촌락 문서의 토지 종목과 면적',url='https://contents.history.go.kr/front/km/view.do?levelId=km_026_0030_0030_0020',role='Comparative registered paddy and dry-field measurements for four villages'),
 'trade_record':dict(institution='National Institute of Korean History',title='청해진 — 한국사 연대기',url='https://contents.history.go.kr/mobile/kc/view.do?code=kc_age_10&levelId=kc_r101460',role='Modern synthesis of the 828 Cheonghaejin foundation and chronology'),
 'jang_source':dict(institution='National Institute of Korean History',title='장보고와 정년 — 사료로 본 한국사',url='https://contents.history.go.kr/front/hm/view.do?levelId=hm_034_0040',role='Primary-source transmission and historiographic commentary on Du Mu, New Book of Tang, Samguk sagi'),
 'market_overview':dict(institution='National Institute of Korean History',title='역대 국사교과서 — unified Silla economy and markets',url='https://contents.history.go.kr/front/ta/view.do?levelId=ta_m51_0050_0010',role='Textbook overview of capital markets, production and Tang commerce; general context, not transaction ledger'),
 'palace_excavation':dict(institution='National Institute of Korean History',title='동궁과 월지 — Silla material culture',url='https://contents.history.go.kr/mobile/eh/view.do?code=ganada&levelId=eh_r0090_0010',role='Educational archaeological account of Wolji and excavated courtly artifacts; not representative of rural society'),
 'festival_primary':dict(institution='National Institute of Korean History',title='가배와 회소곡 — Samguk sagi text and commentary',url='https://contents.history.go.kr/front/hm/view.do?levelId=hm_020_0110',role='Retrospectively transmitted chronicle source; evidence for the Gabae tradition, not a contemporary observation'),
}
SOURCES={
 'IV.3.2':['village_primary','village_analysis','village_critical','festival_primary'],
 'IV.3.5':['village_primary','land_analysis','field_table'],
 'IV.3.6':['market_overview','palace_excavation'],
 'IV.3.7':['trade_record','jang_source','market_overview'],
 'IV.3.8':['palace_excavation','market_overview'],
 'IV.3.9':['village_primary','village_analysis'],
 'IV.3.10':['festival_primary','trade_record'],
}
# Passage indices zero-based. Anchors must align with the actual content of that passage.
CLAIMS={
 'IV.3.2':[(1,'The Silla Village Register records four Seowongyeong-area communities and classifies household members, including dependents.','village_primary','신라의 촌락 지배, register transcription and introductory commentary','direct'),(3,'The Gabae weaving festival is described in a later chronicle, rather than a surviving contemporary village record.','festival_primary','가배와 회소곡, Samguk sagi book 1 excerpt','context')],
 'IV.3.5':[(1,'The four-village register distinguishes rice fields, dry fields, hemp fields, and official field categories.','village_primary','신라의 촌락 지배, registered cultivated fields','direct'),(2,'Recorded paddy and dry-field areas differed substantially among the surviving four villages.','field_table','한국문화사, table 신라 촌락 문서의 토지 종목과 면적','direct')],
 'IV.3.6':[(1,'Silla urban and temple production included textile and metal crafts and specialized manufacturing.','market_overview','역대 국사교과서, 통일 신라 production and trade section','context')],
 'IV.3.7':[(1,'Official histories describe eastern, western, and southern market spaces in Silla’s capital.','market_overview','역대 국사교과서, capital markets passage','context'),(4,'Cheonghaejin is dated to 828 in official historical chronology.','trade_record','청해진, 828 foundation date','direct'),(9,'The Jang Bogo narrative was transmitted through Du Mu and later historical compilers.','jang_source','장보고와 정년, source-transmission commentary','direct')],
 'IV.3.8':[(1,'Wolji was constructed at the Silla court under Munmu around 674, as described in the archaeological overview.','palace_excavation','동궁과 월지, creation of pond and site overview','context')],
 'IV.3.10':[(1,'A later Samguk sagi narrative associates Gabae with communal weaving and feasting.','festival_primary','가배와 회소곡, Korean and classical Chinese source passage','direct')],
}
def parse(path:Path):
 s=path.read_text(encoding='utf8')
 tokens=re.split(r'(?m)^## ([IVX]+\.\d+\.\d+)\s*$',s)
 out={}
 for i in range(1,len(tokens),2):
  key,text=tokens[i],tokens[i+1]
  if key in out:raise ValueError('Duplicate manuscript ID '+key)
  sections=re.split(r'(?m)^### (.+?)\s*$',text)
  blocks=[]
  for j in range(1,len(sections),2):
   heading,body=sections[j],sections[j+1]
   paras=[p.strip() for p in re.split(r'\n\s*\n',body.strip()) if p.strip()]
   if not paras or any(len(p)<120 for p in paras):raise ValueError('Short empty section '+key+' '+heading)
   blocks.append({'title':heading,'paragraphs':paras})
  if len(blocks)<2:raise ValueError('Missing substantial sections '+key)
  out[key]=blocks
 return out

def records():
 a=parse(R/'content/editorial/batch_j_silla_society.md')
 b=parse(R/'content/editorial/batch_j_silla_deepening.md')
 expected={f'IV.3.{i}' for i in range(2,11)}-{ 'IV.3.3','IV.3.4'}
 if set(a)!=expected or set(b)!={'IV.3.1','IV.3.3','IV.3.4'}:raise ValueError('Missing or unexpected IDs '+str((set(a)^expected)|(set(b)^{'IV.3.1','IV.3.3','IV.3.4'})))
 allowed=canonical();result=[];anchors=0;words=0
 for k,blocks in [*a.items(),*b.items()]:
  if k not in allowed:raise ValueError('Not canonical '+k)
  count=sum(len(WORD_RE.findall(p)) for block in blocks for p in block['paragraphs']);words+=count
  if k in a and count<450:raise ValueError('Insufficient new article '+k+': '+str(count))
  if k in ('IV.3.2','IV.3.5','IV.3.7') and count<2000:raise ValueError('Deep treatment below 2000 words: '+k+': '+str(count))
  rec={'id':k,'mode':'replace' if k in a else 'append','blocks':blocks}
  if k in a:
   refs=SOURCES[k];rec.update(release='J',kicker='SILLA SOCIAL HISTORY · COMPLETE CHAPTER',description='An original account connecting social structures, material evidence, and the limits of the surviving record.',sourceStatus='Selected claim-level documentary links; unannotated interpretations are editorial synthesis, not independently peer reviewed.',sources=[REFS[x] for x in refs])
   for passage,claim,ref,locator,kind in CLAIMS.get(k,[]):
    if passage>=len(blocks):raise ValueError('Passage out of range '+k)
    blocks[passage].setdefault('evidence',[]).append({'claim':claim,'sourceIndex':refs.index(ref),'locator':locator,'type':kind});anchors+=1
  result.append(rec)
 return result,{'new_articles':len(a),'deepened_articles':len(b),'authored_words':words,'passages':sum(len(r['blocks']) for r in result),'evidence_anchors':anchors,'longform_words':{k:sum(len(WORD_RE.findall(p)) for x in v for p in x['paragraphs']) for k,v in a.items()}}

def build():
 rec,metrics=records();data=''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in rec)
 if not OUTPUT.exists() or OUTPUT.read_text(encoding='utf8')!=data:OUTPUT.write_text(data,encoding='utf8')
 return metrics
if __name__=='__main__':
 try:print(json.dumps(build(),ensure_ascii=False,indent=2))
 except Exception as exc:print('Batch J rejected:',str(exc),file=sys.stderr);sys.exit(1)
