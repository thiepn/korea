#!/usr/bin/env python3
"""Batch O: preserve authored manuscripts, bind canonical IDs and selectively anchor historical claims."""
from __future__ import annotations
import json,re,sys
from pathlib import Path
from build_corpus import ROOT,WORD_RE,canonical
OUT=ROOT/'content/imports/batch_o_two_chapters.jsonl'
NEW={f'V.5.{x}' for x in (1,2,3,5,7,8,9,10)}|{f'VIII.9.{x}' for x in (1,3,4,5,6,7,8,9,10)}
APPEND={'V.5.4','V.5.6','VIII.9.2','VI.4.3','IX.3.3','VII.5.3','III.3.7','VIII.1.3','IX.1.1'}
LONG={'V.5.3','VIII.9.3','VIII.9.8'}
SOURCES={
 'uicheon':('National Institute of Korean History','대각국사 의천의 천태종 개창 / 사료로 본 한국사','https://contents.history.go.kr/mobile/hm/view.do?levelId=hm_067_0040','Primary excerpts with NIHK analysis; biography of Uicheon and his Song journey; commemorative sources require genre criticism'),
 'cheontae':('Academy of Korean Studies','교장 / 한국민족문화대백과사전','https://encykorea.aks.ac.kr/Article/E0005560','Specialist account cautioning against later terminology that calls the Gyojang an ordinary continuation of the canon'),
 'yesae':('National Institute of Korean History','요세의 백련결사와 천태사상 / 사료로 본 한국사','https://contents.history.go.kr/front/hm/view.do?levelId=hm_067_0100','Epigraphic extract in Dongmunseon with NIHK historical commentary on religious associations'),
 'canon':('Academy of Korean Studies','장경도감 / 한국민족문화대백과사전','https://encykorea.aks.ac.kr/Article/E0048250','Specialist overview of the different canonical printing institutions and their dates'),
 'lantern':('National Institute of Korean History','연등회와 팔관회 / 사료로 본 한국사','https://contents.history.go.kr/front/hm/view.do?levelId=hm_067_0020','Primary Goryeosa quotations on royal lantern and Palgwan ritual; compiled retrospectively'),
 'constitutional':('National Institute of Korean History','대한민국 임시 헌장 (1919.4.11.)','https://contents.history.go.kr/front/hm/view.do?levelId=hm_123_0060&treeId=010701','Primary provisional charter in Korean; ideals do not prove implementation under colonial rule'),
 'constitution':('National Institute of Korean History','대한민국 임시 헌법 (1919.9.11.)','https://contents.history.go.kr/front/hm/view.do?levelId=hm_123_0100','Primary text of revised provisional constitution and scholarly discussion of organizational unification'),
 'march':('National Institute of Korean History','3·1 독립 선언서 / 사료로 본 한국사','https://contents.history.go.kr/mobile/hm/view.do?levelId=hm_123_0040','Primary declaration and contextual commentary on the mass mobilization of 1919'),
 'conference':('National Institute of Korean History','임시정부 개편 노력 / 국민대표회의 선언서 (1923)','https://contents.history.go.kr/front/hm/view.do?levelId=hm_123_0115','Primary declaration and analysis of competing provisional-government reform plans'),
 'finances':('National Institute of Korean History','대한민국임시정부의 어려운 형편 / 백범일지','https://contents.history.go.kr/front/hm/view.do?levelId=hm_126_0055','First-person retrospective memoir excerpt; memory and perspective must be evaluated'),
 'battle':('National Institute of Korean History','봉오동 전투 / 한국사 연대기','https://contents.history.go.kr/mobile/kc/view.do?levelId=kc_i402000','Korean historical overview of 1920 military operations, using later-reported accounts'),
 'armies':('National Institute of Korean History','봉오동·청산리 전투 / 우리역사넷','https://contents.history.go.kr/mobile/ta/view.do?levelId=ta_h62_0040_0030_0040','Legacy textbook overview; useful orientation, not uncritical evidence for disputed casualty totals'),
 'student':('National Institute of Korean History','6·10 만세 운동 격문 / 사료로 본 한국사','https://contents.history.go.kr/mobile/hm/view.do?levelId=hm_124_0030','Primary protest leaflet and commentary on the June Tenth mobilization'),
 'student_history':('National Institute of Korean History','6·10학생운동의 전개 / 신편 한국사','https://contents.history.go.kr/mobile/nh/view.do?levelId=nh_049_0040_0060_0040_0030','Specialist synthesis with dates and organizational specifics; written after the events'),
 'singa':('Academy of Korean Studies','신간회 / 한국민족문화대백과사전','https://encykorea.aks.ac.kr/Article/E0032606','Specialist secondary article on the united front founded in February 1927'),
 'students':('National Institute of Korean History','6·10 만세 운동과 광주 학생 운동 / 우리역사넷','https://contents.history.go.kr/front/ta/view.do?levelId=ta_m31_0110_0030','Broad retrospective treatment of student protest, not a participant diary'),
}
keys={
 'V.5.1':['lantern','canon'],'V.5.2':['uicheon','yesae'],'V.5.3':['uicheon','cheontae','yesae'],
 'V.5.5':['canon'],'V.5.7':['lantern'],'V.5.8':['lantern'],'V.5.9':['lantern'],'V.5.10':['yesae','lantern'],
 'VIII.9.1':['march','constitutional'],'VIII.9.3':['constitutional','constitution','conference','finances'],
 'VIII.9.4':['battle','armies'],'VIII.9.5':['armies'],'VIII.9.6':['march'],
 'VIII.9.7':['singa'],'VIII.9.8':['student','student_history','students'],
 'VIII.9.9':['singa'],'VIII.9.10':['constitution','armies'],
}
# Only grounded, selectively checked claims, attached to the passage that makes the connection.
anchors={
 'V.5.1':[(0,'State ritual sources document Palgwan observances at court in 918; accounts survive in the later Goryeosa compilation.','lantern','『고려사』 팔관회의 / 태조 원년 918년 11월','direct')],
 'V.5.2':[(0,'The NIHK Uicheon source describes doctrinal study and his Song journey as one element of Goryeo Buddhist debates.','uicheon','의천의 천태종 개창, 의천의 교학과 유학','context')],
 'V.5.3':[(0,'Uicheon’s historical collecting program assembled Buddhist commentaries as a body of interpretive scholarship, according to NIHK’s source edition and commentary.','uicheon','대각국사 의천의 천태종 개창, 교장 수집과 교학','context'),(1,'An AKS study identifies the later label Sokjang as a modern historiographical convention for Uicheon’s Gyojang.','cheontae','교장: 명칭 및 1911·1923년 연구사','direct')],
 'V.5.5':[(0,'AKS describes organized Buddhist printing institutions whose work relied upon material resources and state support.','canon','장경도감: 국가 간행 사업과 교장도감','context')],
 'V.5.7':[(0,'Goryeosa ritual entries record Yeondeunhoe ceremonies and shifts in their scheduling.','lantern','『고려사』 권69 상원연등회의, 1010·1058년','direct')],
 'V.5.8':[(0,'Court ritual entries describe events that bound kingship and historical memory.','lantern','『고려사』 연등회 의례 및 태조 기념','context')],
 'V.5.9':[(0,'The Goryeo ritual record is evidence for official celebrations but not proof of uniform private beliefs.','lantern','연등회와 팔관회: 고려사 원문과 국사편찬위원회 해설','context')],
 'V.5.10':[(0,'The Yeose religious-association inscription mentions social participants in a Buddhist network, but it is a commemorative document.','yesae','『동문선』 권117 원묘국사비명 / 결사 참여','context')],
 'VIII.9.1':[(0,'The 1919 declaration framed independence as a public moral claim that circulated under colonial rule.','march','3·1 독립 선언서, 1919년 3월 1일','context')],
 'VIII.9.3':[(0,'The April 1919 provisional charter declares a democratic republic and formal equality.','constitutional','대한민국 임시 헌장 제1조·제3조','direct'),(6,'The September 1919 provisional constitution assigned sovereignty to the Korean people.','constitution','대한민국 임시 헌법 제2조, 1919.9.11','direct')],
 'VIII.9.4':[(0,'The Battle of Bongodong took place in June 1920 and involved Korean independence army formations.','battle','봉오동 전투, 1920년 전투 개요','direct')],
 'VIII.9.5':[(0,'Armed and direct-action initiatives represented only some of the distinct independence strategies of the 1920s.','armies','독립군과 국내외 항일 단체 개관','context')],
 'VIII.9.6':[(0,'The 1919 declaration linked national independence with civil and human dignity, one strand in later education-centered arguments.','march','3·1 독립 선언서, 선언의 원칙','context')],
 'VIII.9.7':[(0,'The 1927 Singanhoe united left nationalists and socialists and operated within a broader colonial social-movement setting.','singa','신간회 연원 및 변천, 1927년 창립','context')],
 'VIII.9.8':[(0,'The June Tenth independence protests occurred in 1926 around Sunjong’s funeral.','student','6·10 만세 운동 격문 / 1926.6.10','direct'),(1,'NIHK documents a continuing student protest tradition culminating in the later Gwangju mobilization.','students','6·10 만세 운동과 광주 학생 운동','context')],
 'VIII.9.9':[(0,'Singanhoe was established in February 1927 as a nationalist-socialist united front.','singa','신간회 연원 및 변천, 1927년 2월','direct')],
 'VIII.9.10':[(0,'Korean independence army activity formed part of a changing, multi-front armed movement beyond the peninsula.','armies','봉오동·청산리 전투 및 해외 독립군 개관','context')],
}

def parse(filename):
 s=(ROOT/'content/editorial'/filename).read_text(encoding='utf8')
 matches=list(re.finditer(r'(?m)^## ((?:[IVX]+)\.\d+\.\d+)\s*$',s));out={}
 for i,m in enumerate(matches):
  key=m[1];section=s[m.end():matches[i+1].start() if i+1<len(matches) else len(s)]
  subtitles=list(re.finditer(r'(?m)^### (.+?)\s*$',section));blocks=[]
  for j,h in enumerate(subtitles):
   segment=section[h.end():subtitles[j+1].start() if j+1<len(subtitles) else len(section)]
   paras=[re.sub(r'\s+',' ',p).strip() for p in re.split(r'\n\s*\n',segment) if p.strip()]
   if not paras or any(len(p)<90 for p in paras):raise ValueError((filename,key,h[1],'invalid paragraph'))
   blocks.append({'title':h[1].strip(),'paragraphs':paras})
  if not blocks or key in out:raise ValueError((filename,key,'duplicate/missing passages'))
  out[key]=blocks
 return out

def build():
 authored={**parse('batch_o_goryeo_religion.md'),**parse('batch_o_independence.md')}
 extensions={**parse('batch_o_deepening.md'),**parse('batch_o_cross_era_deepening.md')}
 expansions=parse('batch_o_long_expansions.md');super_essays=parse('batch_o_super_essays.md')
 if set(authored)!=NEW or set(extensions)!=APPEND or set(expansions)!=LONG or set(super_essays)!=LONG:raise ValueError('Unmatched coverage / duplicates')
 for key in LONG:authored[key]+=expansions[key]+super_essays[key]
 canonical_ids=canonical();counts={};records=[];num_anchors=0
 for key in [*sorted(authored),*sorted(extensions)]:
  if key not in canonical_ids:raise ValueError('Noncanonical '+key)
  blocks=authored.get(key,extensions.get(key));words=sum(len(WORD_RE.findall(p)) for b in blocks for p in b['paragraphs']);counts[key]=words
  if key in LONG and words<2000:raise ValueError(f'Essay {key} only {words} words')
  if key in NEW and words<600:raise ValueError(f'Article {key} only {words} words')
  if key in APPEND and words<400:raise ValueError(f'Append {key} only {words} words')
  source_keys=keys.get(key,[])
  record={'id':key,'mode':'replace' if key in NEW else 'append','blocks':blocks}
  if key in NEW:
   record.update(release='O',kicker='HISTORICAL LIBRARY · CONNECTED HISTORIES',description='Original long-form historical narrative, evidence limits and comparative perspectives.',sourceStatus='Original editorial synthesis with selective Korean-language institutional and historical-source anchors; documentary genres and retrospective accounts differentiated.',sources=[dict(zip(('institution','title','url','role'),SOURCES[k])) for k in source_keys])
   for idx,claim,source_key,loc,kind in anchors.get(key,[]):
    if idx>=len(blocks) or source_key not in source_keys:raise ValueError('Unsupported anchor '+key)
    blocks[idx].setdefault('evidence',[]).append({'claim':claim,'sourceIndex':source_keys.index(source_key),'locator':loc,'type':kind});num_anchors+=1
  records.append(record)
 raw=''.join(json.dumps(r,ensure_ascii=False,separators=(',',':'))+'\n' for r in records)
 if not OUT.exists() or OUT.read_text(encoding='utf8')!=raw:OUT.write_text(raw,encoding='utf8')
 return {'new_articles':len(authored),'append_only_articles':len(extensions),'new_passages':sum(len(r['blocks']) for r in records),'authored_words':sum(counts.values()),'evidence_anchors':num_anchors,'words_by_article':counts}
if __name__=='__main__':
 try:print(json.dumps(build(),ensure_ascii=False,indent=2))
 except Exception as exc:print('ERROR',exc,file=sys.stderr);raise
