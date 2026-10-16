#!/usr/bin/env python3
"""KOREA Batch I: convert authored manuscripts into replay-safe canonical import events.

The markdown is the editable manuscript; this script keeps fixed passages, records
source roles accurately, refuses made-up canonical IDs, and imports append-only.
"""
from __future__ import annotations
import json,re,sys
from pathlib import Path
from build_corpus import canonical,WORD_RE
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'content/imports/batch_i_baekje.jsonl'
SOURCE_PAGES={
 'unesc':dict(institution='UNESCO World Heritage Centre',title='Baekje Historic Areas',url='https://whc.unesco.org/en/list/1477/',role='Archaeological chronology and registered site descriptions, 475–660 CE'),
 'battle371':dict(institution='National Institute of Korean History',title='Historical textbooks: Baekje and the fourth-century northern campaigns',url='https://contents.history.go.kr/front/ta/view.do?levelId=ta_p61_0050_0010_0040',role='Later historical teaching account of Geunchogo’s 371 campaign; chronology contextual not a contemporary report'),
 'hanseong':dict(institution='National Institute of Korean History',title='Baekje royal palaces and Hanseong–Ungjin transition (한국문화사)',url='https://contents.history.go.kr/front/km/print.do?levelId=km_039_0070_0020_0010_0020_0020&whereStr=',role='475 Hanseong collapse, 475–538 Gongju palace context'),
 'gongsanseong':dict(institution='National Institute of Korean History',title='Ungjin period overview (우리역사넷)',url='https://contents.history.go.kr/front/ta/view.do?levelId=ta_h71_0040_0010_0030_0020',role='Kings Dongseong and Muryeong, recovery and Sabi relocation chronology'),
 'inscription':dict(institution='National Research Institute of Cultural Heritage',title='무령왕릉 지석 — Inscription from King Muryeong’s Tomb',url='https://portal.nrich.go.kr/kor/ksmUsrView.do?ksm_idx=2554&menuIdx=584',role='Primary inscription and archaeological context; dates of death and burial'),
 'sabi':dict(institution='Academy of Korean Studies',title='사비천도 — Relocation to Sabi',url='https://encykorea.aks.ac.kr/Article/E0071959',role='538 planned relocation, politics and reform interpretation'),
 'seong':dict(institution='Academy of Korean Studies',title='성왕 — King Seong',url='https://encykorea.aks.ac.kr/Article/E0029457',role='523–554 reign, reform, Sabi, 554 death'),
 'uija':dict(institution='Academy of Korean Studies',title='의자왕 — King Uija',url='https://encykorea.aks.ac.kr/Article/E0043357',role='641–660 reign and scholarly discussion of the fall'),
 'nihs':dict(institution='National Institute of Korean History',title='흑치상지 — Baekje restoration resistance',url='https://contents.history.go.kr/mobile/kc/view.do?code=kc_age_10&levelId=kc_n102100',role='Resistance after the 660 Sabi fall'),
 'museum':dict(institution='National Museum of Korea',title='Baekje Historic Areas of World Heritage exhibition',url='https://www.museum.go.kr/ENG/contents/E0202030000.do?exhiSpThemId=113856&listType=list&menuId=past&schM=view',role='Gongju, Buyeo, Iksan sites and 475–660 chronology'),
}
SOURCES={
 'III.2.1':['hanseong','unesc','battle371'], 'III.2.3':['hanseong','museum'],
 'III.2.4':['unesc','museum'], 'III.2.6':['hanseong','gongsanseong','unesc'],
 'III.2.7':['gongsanseong','inscription'], 'III.2.8':['inscription','unesc','museum'],
 'III.2.9':['sabi','seong','unesc'], 'III.2.10':['uija','nihs','unesc'],
}
# Passage ordinal (1-based), claim, source key, locator, kind.  Specific sites
# are provided to readers; `context` is never misrepresented as full proof.
EVIDENCE={
 'III.2.1':[(7,'The early expansion tradition includes a 371 battle in which Goguryeo king Gogukwon died','battle371','NIHK historical textbook narrative, Geunchogo paragraph; later retrospective account','context')],
 'III.2.3':[(1,'The Hanseong capital zone included major earthworks and a river-linked administrative landscape','hanseong','NIHK palace history, early Baekje capital descriptions and Pungnap discussion','context')],
 'III.2.6':[(1,'Hanseong fell to Goguryeo attack in 475 and King Gaero died during the crisis','hanseong','NIHK 한국문화사, Ungjin-period palace subsection, introduction','direct'),(5,'Baekje relocated its capital to the Ungjin Gongju region in 475','unesc','UNESCO Historic Areas listing, Ungjin period 475–538 CE','direct')],
 'III.2.7':[(3,'Muryeong died in 523 and was formally interred in 525 according to the excavated inscription','inscription','NRICH 무령왕릉 지석, inscription overview and king epitaph','direct')],
 'III.2.8':[(1,'The tomb of King Muryeong was discovered in 1971 with name-bearing stone inscriptions','inscription','NRICH inscription entry, overview of 1971 discovery and finds','direct'),(3,'The inscription records Muryeong’s death in 523 and burial in 525','inscription','NRICH king inscription, death and burial date translation','direct'),(4,'The tomb’s brick chamber and related grave goods show southern Chinese influences','inscription','NRICH archaeological description of brick chamber and furnishings','context')],
 'III.2.9':[(1,'King Seong moved Baekje’s capital from Ungjin to Sabi in 538','sabi','AKS 사비천도 entry, date and results','direct'),(3,'King Seong undertook state reorganization and died during the 554 conflict','seong','AKS 성왕 biography, reforms and last years','direct')],
 'III.2.10':[(2,'Uija ruled Baekje from 641 until the Sabi defeat of 660','uija','AKS 의자왕 biography, reign and fall','direct'),(5,'Armed Baekje restoration movements continued after the royal collapse of 660','nihs','NIHK 흑치상지, Baekje restoration movement section','direct')],
}
def parse(path):
    raw=path.read_text(encoding='utf-8')
    entries=re.split(r'(?m)^## ([IVX]+\.\d+\.\d+)\s*$',raw)
    out={}
    for i in range(1,len(entries),2):
        key,part=entries[i:i+2]
        sub=re.split(r'(?m)^### (.+?)\s*$',part)
        blocks=[]
        for j in range(1,len(sub),2):
            title,text=sub[j:j+2]
            paras=[p.strip() for p in re.split(r'\n\s*\n',text.strip()) if p.strip()]
            if not paras or any(len(p)<120 for p in paras):raise ValueError(f'Insufficient manuscript paragraph: {key}: {title}')
            blocks.append({'title':title,'paragraphs':paras})
        if not blocks or key in out:raise ValueError(f'Duplicate / empty section: {key}')
        out[key]=blocks
    return out

def records():
    c=canonical(); new=parse(ROOT/'content/editorial/batch_i_baekje_collection.md'); app=parse(ROOT/'content/editorial/batch_i_deepening.md')
    if set(new)!=set(SOURCES):raise ValueError(f'Missing or unexpected Baekje article: {set(new)^set(SOURCES)}')
    if set(new)&set(app):raise ValueError('Overlap of replacement and append manuscripts')
    if not all(x in c for x in new|app):raise ValueError('Unknown canonical ID')
    results=[];refs=0;word_total=0
    for k,blocks in list(new.items())+list(app.items()):
        word_total+=sum(len(WORD_RE.findall(p)) for b in blocks for p in b['paragraphs'])
        rec={'id':k,'mode':'append' if k in app else 'replace','blocks':blocks}
        if k in new:
            rec.update({'kicker':'IN-DEPTH HISTORY' if len(blocks)>=8 else 'BAEKJE: COMPLETE CHAPTER', 'release':'I','description':'Original historical synthesis with explicitly identified institutional and primary-source anchors; interpretations have not been independently peer-reviewed.', 'sourceStatus':'Selective primary and institutional sources; broader prose editorial synthesis not line-by-line verified', 'sources':[SOURCE_PAGES[x] for x in SOURCES[k]]})
            for ordinal,claim,ref,locator,kind in EVIDENCE.get(k,[]):
                if not 1<=ordinal<=len(blocks):raise ValueError(f'Invalid passage locator {k}/{ordinal}')
                blocks[ordinal-1].setdefault('evidence',[]).append({'claim':claim,'sourceIndex':SOURCES[k].index(ref),'locator':locator,'type':kind})
                refs+=1
        results.append(rec)
    return results,word_total,refs

def build():
    records_list,word_total,refs=records()
    raw='\n'.join(json.dumps(x,ensure_ascii=False,separators=(',',':')) for x in records_list)+'\n'
    if not OUT.exists() or OUT.read_text(encoding='utf-8')!=raw:OUT.write_text(raw,encoding='utf-8')
    return {'new_articles':len(SOURCES),'deepened_articles':len(records_list)-len(SOURCES),'authored_words':word_total,'new_passages':sum(len(r['blocks']) for r in records_list),'evidence_anchors':refs}
if __name__=='__main__':print(json.dumps(build(),indent=2))
