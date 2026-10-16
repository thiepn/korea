#!/usr/bin/env python3
"""Batch M: author-curated later-Joseon family texts, bounded source anchors, replay-safe JSONL."""
from __future__ import annotations
import json,re,sys
from pathlib import Path
from build_corpus import WORD_RE,canonical
R=Path(__file__).resolve().parents[1]
OUT=R/'content/imports/batch_m_later_joseon_households.jsonl'
DEEP_IDS={'VII.5.1','VII.5.4','VII.5.9'}
NEW_IDS={f'VII.5.{i}' for i in (1,4,5,6,7,8,9,10)}
APPEND_IDS={'VII.5.2','VII.5.3'}
REF={
'genealogy':dict(institution='Academy of Korean Studies',title='족보 — 한국민족문화대백과사전',url='https://encykorea.aks.ac.kr/Article/E0052821',role='Secondary scholarly account; compares early inclusive and later agnatic genealogical structures'),
'patriarchy':dict(institution='Academy of Korean Studies',title='가부장제 — 한국민족문화대백과사전',url='https://encykorea.aks.ac.kr/Article/E0000200',role='Secondary historical synthesis of female agency and later patrilineal consolidation'),
'partition':dict(institution='Academy of Korean Studies',title='분재기 — 한국민족문화대백과사전',url='https://encykorea.aks.ac.kr/Article/E0024857',role='Document genre description for actual property transfers and family inheritance'),
'gift':dict(institution='Academy of Korean Studies',title='별급문기 — 한국민족문화대백과사전',url='https://encykorea.aks.ac.kr/Article/E0023006',role='Surviving period document genre for separate property gifts; not a universal pattern'),
'family':dict(institution='Academy of Korean Studies',title='조선 — 가족과 친족',url='https://encykorea.aks.ac.kr/Article/E0051904',role='Secondary contextual synthesis of family, rites and hierarchy'),
'marriage':dict(institution='Academy of Korean Studies',title='혼인 — 한국민족문화대백과사전',url='https://encykorea.aks.ac.kr/Article/E0063911',role='Institutional chronology and restrictions, not all lived marriage practices'),
'house':dict(institution='Academy of Korean Studies',title='안채 — 한국민족문화대백과사전',url='https://encykorea.aks.ac.kr/Article/E0071924',role='Historical architecture study of anchae and later sarangchae spatial differentiation'),
'housecase':dict(institution='Academy of Korean Studies',title='안동 하회 양진당 — surviving upper-status residential complex',url='https://encykorea.aks.ac.kr/Article/E0034647',role='Material architecture example, not representative of all Joseon houses'),
'painting':dict(institution='National Institute of Korean History',title='풍속화 — 조선 후기 생활의 시각 자료',url='https://contents.history.go.kr/mobile/kc/view.do?code=kc_age_30&levelId=kc_r300850',role='Secondary interpretation of genre paintings; representations are not census data'),
'physicians':dict(institution='Academy of Korean Studies',title='의녀 — 한국민족문화대백과사전',url='https://encykorea.aks.ac.kr/Article/E0043144',role='Institutional history of women medical practitioners, including 1406 establishment'),
'medexam':dict(institution='Academy of Korean Studies',title='의과 — 한국민족문화대백과사전',url='https://encykorea.aks.ac.kr/Article/E0043125',role='Historical medical examination and relevant institutions'),
'rites':dict(institution='Academy of Korean Studies',title='사례 — 관혼상제와 변화',url='https://encykorea.aks.ac.kr/Article/E0025508',role='Secondary account of shifting ritual priorities including ancestral rites and mourning'),
'funeral':dict(institution='Academy of Korean Studies',title='상례 — 한국민족문화대백과사전',url='https://encykorea.aks.ac.kr/Article/E0027059',role='Historical conceptual description of funeral rites'),
}
SOURCES={
'VII.5.1':['genealogy','patriarchy','partition','gift','rites'],
'VII.5.4':['family','patriarchy','painting'],
'VII.5.5':['family','partition','gift'],
'VII.5.6':['house','housecase'],
'VII.5.7':['painting','family'],
'VII.5.8':['painting','family'],
'VII.5.9':['physicians','medexam','family'],
'VII.5.10':['rites','funeral','family'],
}
# block index, factual anchor, source key, locator, source strength
ANCHORS={
'VII.5.1':[(1,'The format of Korean genealogies shifted from emphasizing varied affinal ties toward a stronger male-line organization.','genealogy','조선 전기 족보의 특징 / 조선 후기의 족보','direct'),(5,'Joseon family property was documented in division papers that specified recipients and distributions.','partition','분재기, 종류 및 문서 구성','direct'),(5,'A separate gift document could mark marriage, examination success, recovery from illness and other special circumstances.','gift','별급문기, 별급 사유와 문서 양식','direct'),(7,'Ancestral ritual succession became an increasingly emphasized element of later Joseon Confucian kinship.','rites','사례, 제례 변화와 장자 중심 봉사','context')],
'VII.5.4':[(3,'Confucian moral expectations coexisted with significant historical changes in kinship and women’s family roles.','patriarchy','가부장제, 가족제도의 역사적 변천','context')],
'VII.5.5':[(2,'Inheritance documents could list land and enslaved people as transferrable estate assets.','partition','분재기, 분배 대상 및 문서 양식','context')],
'VII.5.6':[(1,'The distinction between the anchae and sarangchae strengthened in later Joseon housing patterns.','house','안채, 연원 및 변천 / 사랑채의 분화' ,'direct'),(4,'Yangjindang at Hahoe is a documented upper-status complex with anchae, sarangchae, and associated buildings.','housecase','안동 하회 양진당, 건물 구성','direct')],
'VII.5.7':[(3,'Genre paintings from later Joseon depict varied work, leisure and household activity, though as selective representations.','painting','풍속화, 대표 작품과 사료 해석','context')],
'VII.5.8':[(4,'Images of everyday life must be interpreted as genre representations rather than a statistically typical national wardrobe.','painting','풍속화, 기록성과 미술적 구성','context')],
'VII.5.9':[(2,'Female medical practitioners were formally instituted in 1406 to address constraints on examining women.','physicians','의녀, 연혁 / 1406년 제생원','direct'),(1,'Medical examinations were used to select officials for the medical bureaus of Joseon.','medexam','의과, 시행 대상과 소속 기관','direct')],
'VII.5.10':[(1,'Later Confucian four-rites practice intensified mourning and ancestral worship organized through the principal male heir.','rites','사례, 상례와 제례 변천','context'),(0,'Funeral rites concerned both treatment of the deceased and restoration of kinship obligations among survivors.','funeral','상례, 정의 및 절차 / 가계의 계승' ,'context')],
}
def parse(path):
 t=path.read_text(encoding='utf8');matches=list(re.finditer(r'(?m)^## (VII\.5\.\d+)\s*$',t));out={}
 for i,m in enumerate(matches):
  body=t[m.end():matches[i+1].start() if i+1<len(matches) else len(t)]
  sections=list(re.finditer(r'(?m)^### ([^\n]+)\s*$',body))
  blocks=[]
  for j,s in enumerate(sections):
   chunk=body[s.end():sections[j+1].start() if j+1<len(sections) else len(body)]
   paras=[p.strip().replace('\n',' ') for p in re.split(r'\n\s*\n',chunk) if len(p.strip())>0]
   if not paras or any(len(p)<40 for p in paras):raise ValueError('Malformed prose '+m[1]+':'+s[1])
   blocks.append({'title':s[1].strip(),'paragraphs':paras})
  if not blocks:raise ValueError('No passages '+m[1])
  out[m[1]]=blocks
 return out
def build():
 new={**parse(R/'content/editorial/batch_m_deep.md'),**parse(R/'content/editorial/batch_m_collections.md')}
 extra=parse(R/'content/editorial/batch_m_deepening.md')
 if set(new)!=NEW_IDS or set(extra)!=APPEND_IDS:raise ValueError('Unexpected canonical article IDs')
 canonical_ids=canonical();rows=[];counts={};anchors=0
 for key,blocks in [*new.items(),*extra.items()]:
  if key not in canonical_ids:raise ValueError('Unknown ID '+key)
  n=sum(len(WORD_RE.findall(p)) for block in blocks for p in block['paragraphs']);counts[key]=n
  if key in DEEP_IDS and n<2000:raise ValueError(f'Deep article below 2000: {key}: {n}')
  if key in NEW_IDS-DEEP_IDS and n<400:raise ValueError(f'New article below 400: {key}: {n}')
  if key in APPEND_IDS and n<180:raise ValueError(f'Append article below 180: {key}: {n}')
  record={'id':key,'mode':'replace' if key in NEW_IDS else 'append','blocks':blocks}
  if key in NEW_IDS:
   sources=SOURCES[key]
   record.update(release='M',kicker='LATER JOSEON · HOUSEHOLD HISTORY',description='Original social history of kinship, work, care and everyday lives in later Joseon.',sourceStatus='Editorial historical synthesis with selective, claim-level contextual and institutional sources; not independently reviewed sentence by sentence.',sources=[REF[k] for k in sources])
   for index,claim,source,locator,kind in ANCHORS.get(key,[]):
    if index>=len(blocks):raise ValueError(f'Evidence section absent {key}:{index}')
    blocks[index].setdefault('evidence',[]).append({'claim':claim,'sourceIndex':sources.index(source),'locator':locator,'type':kind});anchors+=1
  rows.append(record)
 OUT.parent.mkdir(parents=True,exist_ok=True)
 blob=''.join(json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n' for row in rows)
 if not OUT.exists() or OUT.read_text(encoding='utf8')!=blob:OUT.write_text(blob,encoding='utf8')
 return dict(new_articles=len(new),deepened_articles=len(extra),new_passages=sum(len(r['blocks']) for r in rows),authored_words=sum(counts.values()),anchors=anchors,words_by_article=counts)
if __name__=='__main__':
 try:print(json.dumps(build(),ensure_ascii=False,indent=2))
 except Exception as exc:print('Batch M FAILED',exc,file=sys.stderr);raise SystemExit(1)
