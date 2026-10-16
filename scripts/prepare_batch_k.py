#!/usr/bin/env python3
"""Batch K: evidence-aware, append-only Gojoseon corpus edition.

Do not infer one early state's territory from Bronze Age objects; do not treat
medieval foundation traditions as prehistoric eyewitness testimony.
"""
from __future__ import annotations
import json,sys,re
from pathlib import Path
from prepare_batch_j import parse
from build_corpus import WORD_RE,canonical
ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'content/imports/batch_k_gojoseon.jsonl'
REF={
 'NIKH_ORIGINS':{'institution':'National Institute of Korean History','title':'신편 한국사 — 고조선의 명칭과 성립','url':'https://contents.history.go.kr/front/nh/view.do?levelId=nh_004_0030_0010_0010','role':'Modern historical analysis of the name, early statehood, medieval sources and divergent periodization'},
 'NIKH_GEO':{'institution':'National Institute of Korean History','title':'신편 한국사 — 고조선의 위치와 강역','url':'https://contents.history.go.kr/front/nh/view.do?levelId=nh_004_0030_0010_0050','role':'Review of Liaodong, Pyongyang and migration hypotheses, textual chronology and disputed geography'},
 'NIKH_GROWTH':{'institution':'National Institute of Korean History','title':'사료로 본 한국사 — 고조선의 성장과 변화 (魏略 in 三國志)','url':'https://contents.history.go.kr/front/hm/view.do?levelId=hm_001_0020','role':'Transmitted primary-text excerpt on royal titles, diplomacy and the Yan Qin Kai attack; compiled through later authors'},
 'NIKH_POLITY':{'institution':'National Institute of Korean History','title':'사료로 본 한국사 — 고조선의 정치구조 (史記 and 魏略)','url':'https://contents.history.go.kr/front/hm/view.do?levelId=hm_001_0040','role':'Transmitted primary-text passage identifying the named late court officials and defection narrative'},
 'NIKH_DANGUN':{'institution':'National Institute of Korean History','title':'한국사 연대기 — 단군 (三國遺事)','url':'https://contents.history.go.kr/mobile/kc/view.do?code=kc_age_10&levelId=kc_n100800','role':'Secondary chronology of the medieval recording of the foundation story, with source and motifs'},
 'NIKH_MEMORY':{'institution':'National Institute of Korean History','title':'신편 한국사 — 조선 초기 단군조선·기자조선의 역사화','url':'https://contents.history.go.kr/mobile/nh/view.do?levelId=nh_026_0020_0030_0010_0010_0010','role':'Early Joseon commemoration of Dangun and Gija; evidence for later ritual, not Bronze Age events'},
 'AKS_GOJOSEON':{'institution':'Academy of Korean Studies','title':'고조선 — 한국민족문화대백과사전','url':'https://encykorea.aks.ac.kr/Article/E0003937','role':'Scholarly synthesis of early centers, bronze dagger assemblages and debate; some placements are contested'},
 'AKS_JIZI':{'institution':'Academy of Korean Studies','title':'기자조선 — 한국민족문화대백과사전','url':'https://encykorea.aks.ac.kr/Article/E0008396','role':'Historical critique and legacy of the Gija/Jizi migration and dynastic tradition'},
 'AKS_LIAONING':{'institution':'Academy of Korean Studies','title':'요령 정가와자 유적 — 한국민족문화대백과사전','url':'https://encykorea.aks.ac.kr/Article/E0039316','role':'Liaoning archaeology, chronology and alternative cultural-political attributions'},
}
SOURCES={
 'II.1.1':['NIKH_ORIGINS','NIKH_GEO','NIKH_GROWTH','AKS_GOJOSEON'],
 'II.1.3':['AKS_JIZI','NIKH_MEMORY','NIKH_ORIGINS'],
 'II.1.5':['NIKH_GEO','AKS_GOJOSEON','AKS_LIAONING'],
 'II.1.6':['NIKH_GROWTH','NIKH_POLITY','AKS_LIAONING'],
 'II.1.8':['NIKH_GROWTH','NIKH_GEO','AKS_GOJOSEON'],
 'II.1.9':['AKS_LIAONING','NIKH_ORIGINS','AKS_GOJOSEON'],
 'II.1.10':['NIKH_DANGUN','NIKH_MEMORY','NIKH_ORIGINS','AKS_JIZI'],
}
# Each direct claim is about the PRESENCE in a source, not proof that the event occurred as transmitted.
EVIDENCE={
 'II.1.1':[(2,'The Weilüe tradition survives in later citation and depicts titled rulers and diplomacy with Yan.','NIKH_GROWTH','魏略 quotation in 三國志 vol.30, section 고조선의 성장과 변화','direct'),(5,'Scholars have offered competing Liaodong, Pyongyang, and movement reconstructions for the center.','NIKH_GEO','고조선의 위치와 강역, subsection 위치문제','context')],
 'II.1.3':[(0,'Gija/Jizi became a formative narrative in later Joseon origin and governance traditions.','AKS_JIZI','기자조선, concept and historiographical dispute','context'),(2,'Early Joseon officials debated commemoration of Dangun and Gija in state ritual.','NIKH_MEMORY','조선 초기 역사학 subsection 단군조선·기자조선','context')],
 'II.1.5':[(1,'Historical scholarship records competing hypotheses about Gojoseon centers and geographical boundaries.','NIKH_GEO','고조선의 위치와 강역, (1) 고조선의 위치문제','context')],
 'II.1.6':[(1,'A transmitted Weilüe passage depicts a Joseon ruler claiming royal title and sending envoys amid tensions with Yan.','NIKH_GROWTH','위략 cited in 삼국지 30, 고조선의 성장과 변화','direct'),(7,'The Shiji describes named Joseon ministers and military officials during the late Han conflict.','NIKH_POLITY','史記 vol.115, 朝鮮列傳, political-structure excerpt','direct')],
 'II.1.8':[(0,'The transmitted record names Qin Kai as the Yan commander responsible for a Joseon frontier offensive.','NIKH_GROWTH','魏略 in 三國志 vol.30, 고조선의 성장과 변화','direct')],
 'II.1.9':[(2,'Liaoning grave assemblages support analyses of prestige display but their political attribution is interpreted.','AKS_LIAONING','요령 정가와자 유적, excavation and scholarly interpretation','context')],
 'II.1.10':[(1,'Samguk yusa transmitted a Dangun story in a medieval compilation rather than in a prehistoric chronicle.','NIKH_DANGUN','단군, section 삼국유사에 기록된 단군신화','context'),(4,'Early Joseon court discussions addressed official sacrifices to Dangun and Gija.','NIKH_MEMORY','조선 초기, state ritual after 1392','context')],
}

def parse_append(path):
    text=path.read_text(encoding='utf-8')
    sections=re.split(r'(?m)^## (II\.1\.\d+)\s*$',text)
    result={}
    for i in range(1,len(sections),2):
        key,body=sections[i],sections[i+1]
        pieces=re.split(r'(?m)^### (.+?)\s*$',body)
        blocks=[]
        for j in range(1,len(pieces),2):
            para=pieces[j+1].strip()
            if len(para)<150:raise ValueError('Too short append section '+key)
            blocks.append({'title':pieces[j],'paragraphs':[para]})
        if not blocks:raise ValueError('Empty append '+key)
        result[key]=blocks
    return result

def records():
    long=parse(ROOT/'content/editorial/batch_k_gojoseon_deep.md')
    short=parse(ROOT/'content/editorial/batch_k_gojoseon_collections.md')
    append=parse_append(ROOT/'content/editorial/batch_k_gojoseon_deepening.md')
    all_new={**long,**short}
    expected={f'II.1.{n}' for n in (1,3,5,6,8,9,10)}
    if set(all_new)!=expected or set(append)!={'II.1.2','II.1.4','II.1.7'}:
        raise ValueError('Mismatch from canonical Chapter II.1 available subjects')
    if len(long)!=3 or any(k not in long for k in ('II.1.1','II.1.6','II.1.10')):raise ValueError('Missing substantive essays')
    allowed=canonical();records=[];counts={};total=0;anchors=0
    for key,blocks in list(all_new.items())+list(append.items()):
        if key not in allowed:raise ValueError('Noncanonical '+key)
        words=sum(len(WORD_RE.findall(p)) for block in blocks for p in block['paragraphs'])
        if key in long and words<2000:raise ValueError(f'Less than 2000 authored words for {key}: {words}')
        if key in short and words<500:raise ValueError(f'Insufficient distinct short subject {key}: {words}')
        if key in append and words<125:raise ValueError(f'Insufficient append {key}: {words}')
        total+=words;counts[key]=words
        event={'id':key,'mode':'replace' if key in all_new else 'append','blocks':blocks}
        if key in all_new:
            references=SOURCES[key]
            event.update(release='K',kicker='GOJOSEON · SOURCES AND REGIONAL HISTORY',description='Original historical synthesis distinguishing material evidence, transmitted sources and debated modern reconstructions.',sourceStatus='Selective direct/contextual citations; unresolved chronology, geography and broader interpretation not independently peer reviewed.',sources=[REF[x] for x in references])
            for b,claim,ref,locator,kind in EVIDENCE.get(key,[]):
                if b>=len(blocks):raise ValueError('Evidence passage out of bounds')
                blocks[b].setdefault('evidence',[]).append({'claim':claim,'sourceIndex':references.index(ref),'locator':locator,'type':kind});anchors+=1
        records.append(event)
    return records,{'new_articles':len(all_new),'deepened_articles':len(append),'new_passages':sum(len(r['blocks']) for r in records),'authored_words':total,'anchors':anchors,'word_counts':counts}

def build():
    rows,metrics=records()
    body=''.join(json.dumps(r,ensure_ascii=False,separators=(',',':'))+'\n' for r in rows)
    OUTPUT.parent.mkdir(exist_ok=True,parents=True)
    if not OUTPUT.exists() or OUTPUT.read_text(encoding='utf-8')!=body:OUTPUT.write_text(body,encoding='utf-8')
    return metrics
if __name__=='__main__':
    try:print(json.dumps(build(),ensure_ascii=False,indent=2))
    except Exception as exc:print('BATCH K PREPARE REJECTED:',exc,file=sys.stderr);sys.exit(1)
