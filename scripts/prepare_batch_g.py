#!/usr/bin/env python3
"""Batch G: source-first Silla Chapter III.3 and append-only deepening.

All new addresses must be canonical. No previous prose is altered. Reference
metadata is scoped to explicit documented factual anchors and honest context.
"""
from pathlib import Path
import sys,json,re
from prepare_editorial import prepare
from build_corpus import canonical,DATA,WORD_RE
ROOT=Path(__file__).resolve().parents[1]
NEW={f'III.3.{x}' for x in [1,3,4,7,8,9,10]}
DEEP={f'VI.4.{x}' for x in range(5,11)}|{f'IX.3.{x}' for x in range(5,11)}
OUT=ROOT/'content/imports/batch_g_collections.jsonl'
REFERENCES={
 'silla':{'institution':'Academy of Korean Studies','title':'Silla (신라), Encyclopedia of Korean Culture','url':'https://encykorea.aks.ac.kr/Article/E0032800','role':'General historical framework and succession; contextual, not a direct certification of interpretation'},
 'gyeongju':{'institution':'UNESCO World Heritage Centre','title':'Gyeongju Historic Areas','url':'https://whc.unesco.org/en/list/976/','role':'Documented archaeological monuments, tomb groups and Hwangnyongsa and Bunhwangsa buildings'},
 'naemul':{'institution':'Academy of Korean Studies','title':'Naemul Maripgan (내물마립간)','url':'https://encykorea.aks.ac.kr/Article/E0012440','role':'Reign, Kim dynasty consolidation and relations with Goguryeo'},
 'stele':{'institution':'Academy of Korean Studies','title':'Gwanggaeto Stele (광개토왕릉비)','url':'https://encykorea.aks.ac.kr/Article/E0005058','role':'Inscription account of Silla appeal and the 400 campaign; interpretations contested'},
 'jinheung':{'institution':'Academy of Korean Studies','title':'King Jinheung (진흥왕)','url':'https://encykorea.aks.ac.kr/Article/E0055013','role':'Reign 540–576, expansion and court-sponsored historical compilation'},
 'inspection':{'institution':'Academy of Korean Studies','title':'Jinheung Royal Inspection Steles (진흥왕 순수비)','url':'https://encykorea.aks.ac.kr/Article/E0055015','role':'Four preserved steles and their geographical and political significance'},
 'bone':{'institution':'Academy of Korean Studies','title':'Bone-Rank System (골품제도)','url':'https://encykorea.aks.ac.kr/Article/E0004196','role':'Rank and social restrictions, with questions of periodization'},
 'seondeok':{'institution':'Academy of Korean Studies','title':'Queen Seondeok (선덕여왕)','url':'https://encykorea.aks.ac.kr/Article/E0028652','role':'Reign, Daeya fortress, Buddhist building patronage and political crisis'},
 'muyeol':{'institution':'Academy of Korean Studies','title':'King Taejong Muyeol / Kim Chunchu (태종무열왕)','url':'https://encykorea.aks.ac.kr/Article/E0059042','role':'Diplomacy, kinship alliances, Daeya and accession'},
 'yushin':{'institution':'Academy of Korean Studies','title':'Kim Yushin (김유신)','url':'https://encykorea.aks.ac.kr/Article/E0010086','role':'Gaya ancestry, military leadership, alliance with Chunchu'},
}
META={
 'III.3.1':(['silla','gyeongju'],('The Silla kingdom emerged from the southeastern Gyeongju region.',0,'Overview and historical setting','context')),
 'III.3.3':(['stele','naemul'],('The Gwanggaeto inscription records Silla’s request and a major Goguryeo intervention in 400.',0,'Inscription entry: 399 request and 400 campaign','direct')),
 'III.3.4':(['silla','gyeongju'],('The Gyeongju tumuli contain elaborate elite grave goods, including gold and imported material.',1,'Tumuli Park Belt archaeological description','direct')),
 'III.3.7':(['jinheung','inspection'],('Four surviving Jinheung royal inspection steles document mid-sixth-century territorial expansion.',1,'Summary of four inspection inscriptions','direct')),
 'III.3.8':(['bone','yushin'],('Bone rank imposed hereditary restrictions on office, marriage, housing and public dress.',0,'Definition and nature of the bone-rank system','direct')),
 'III.3.9':(['seondeok','gyeongju'],('Seondeok reigned from 632 to 647 and faced the fall of Daeya fortress in 642.',2,'Queen Seondeok: events of 642 and reign','direct')),
 'III.3.10':(['muyeol','yushin'],('Kim Chunchu succeeded to the throne in 654 and was allied politically with Kim Yushin.',3,'Accession and political alliance with Kim Yushin','direct')),
}

def deepening():
 titles=canonical();items=[];current=None;block=None
 for raw in (ROOT/'content/editorial/batch_g_deepening.md').read_text(encoding='utf-8').splitlines():
  line=raw.strip()
  if line.startswith('## '):
   key=line[3:].strip()
   if key not in DEEP or key not in titles or any(x['id']==key for x in items):raise ValueError('Invalid deepening canonical ID '+key)
   if not (DATA/'articles'/f'{key}.json').is_file():raise ValueError('Missing published foundation: '+key)
   current={'id':key,'mode':'append','blocks':[]};items.append(current);block=None
  elif line.startswith('### '):
   if current is None:raise ValueError('Passage before canonical ID')
   block={'title':line[4:].strip(),'paragraphs':[]};current['blocks'].append(block)
  elif line and not line.startswith('#'):
   if block is None:continue
   if len(WORD_RE.findall(line))<40:raise ValueError('Incomplete prose passage: '+current['id'])
   block['paragraphs'].append(line)
 if {x['id'] for x in items}!=DEEP:raise ValueError('Incomplete deepening addresses')
 if any(len(x['blocks'])!=1 or len(x['blocks'][0]['paragraphs'])!=2 for x in items):raise ValueError('Unexpected deepening structure')
 return items

def build(write=True):
 scratch=OUT.with_suffix('.tmp')
 prepare(ROOT/'content/editorial/batch_g_silla.md',scratch,release='G',allow_existing=True)
 fresh=[json.loads(s) for s in scratch.read_text(encoding='utf-8').splitlines() if s]
 scratch.unlink()
 if {x['id'] for x in fresh}!=NEW:raise ValueError('Missing canonical Silla topic')
 for x in fresh:
  refs,claim=META[x['id']]; x.update(kicker='SILLA · COMPLETE CHAPTER',description='A new chapter-scale original synthesis; selected factual anchors have institutional sources, interpretations and uncertainties remain editorial.',sourceStatus='Specific claims are marked with institutional references; the remaining essay is interpretive synthesis, not claim-by-claim peer review.',sources=[REFERENCES[k] for k in refs])
  words=sum(len(WORD_RE.findall(p)) for b in x['blocks'] for p in b['paragraphs'])
  if words<525 or len(x['blocks'])!=4 or any(len(b['paragraphs'])!=2 for b in x['blocks']):raise ValueError('Too short to publish: '+x['id'])
  claimtext,passage,locator,kind=claim
  # Some claim metadata references the second source; the citation must map accurately.
  source_idx=1 if x['id'] in ('III.3.4','III.3.7') else 0
  x['blocks'][passage]['evidence']=[{'claim':claimtext,'sourceIndex':source_idx,'locator':locator,'type':kind}]
 expanded=deepening();batch=fresh+expanded
 raw=''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in batch)
 if write:OUT.write_text(raw,encoding='utf-8')
 return {'new':len(fresh),'append':len(expanded),'passages':sum(len(x['blocks']) for x in batch),'words':sum(len(WORD_RE.findall(p)) for x in batch for b in x['blocks'] for p in b['paragraphs']),'direct_claims':sum(len(b.get('evidence',[])) for x in fresh for b in x['blocks'])}
if __name__=='__main__':print(json.dumps(build(),indent=2))
