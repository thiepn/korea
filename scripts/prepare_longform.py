#!/usr/bin/env python3
"""Convert editorial Markdown to a replay-safe import batch with provenance metadata.

Markdown uses ## canonical ID, ### individual passage title, then paragraphs.
The source manuscript and research registry are kept outside public dist.
Refuses under-length essays, empty passages, duplicate headings or unsupported IDs.
"""
from pathlib import Path
import json,re,sys
from build_corpus import canonical,WORD_RE
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'content/editorial/batch_e_longform.md'
DEST=ROOT/'content/imports/batch_e_longform.jsonl'
PROVENANCE=ROOT/'content/research/batch_e_sources.json'

def run():
    document=SOURCE.read_text(encoding='utf8')
    anchors=list(re.finditer(r'^## ([IVX]+\.\d+\.\d+)\s*$',document,re.M))
    if not anchors:raise ValueError('Missing canonical manuscripts')
    titles=canonical();registry=json.loads(PROVENANCE.read_text(encoding='utf8'))['articles']
    records=[];stats={};used=set()
    for i,anchor in enumerate(anchors):
        key=anchor.group(1)
        if key in used or key not in titles:raise ValueError('Repeated/invalid canonical article '+key)
        used.add(key)
        section=document[anchor.end():anchors[i+1].start() if i+1<len(anchors) else len(document)]
        headings=list(re.finditer(r'^### (.+)$',section,re.M))
        blocks=[]
        for j,heading in enumerate(headings):
            title=heading.group(1).strip();body=section[heading.end():headings[j+1].start() if j+1<len(headings) else len(section)]
            paragraphs=[p.strip().replace('\n',' ') for p in re.split(r'\n\s*\n',body.strip()) if p.strip()]
            if len(paragraphs)<2 or any(len(WORD_RE.findall(p))<55 for p in paragraphs):raise ValueError(key+': thin/empty paragraph in '+title)
            if title in [x['title'] for x in blocks]:raise ValueError('Duplicate passage title '+key)
            blocks.append({'title':title,'paragraphs':paragraphs})
        count=sum(len(WORD_RE.findall(p)) for b in blocks for p in b['paragraphs'])
        if count<2000 or len(blocks)<6:raise ValueError(f'{key}: fewer than 2000 original words or six passages: {count}')
        if key not in registry or len(registry[key].get('sources',[]))<2:raise ValueError(key+': missing research registry')
        r={'id':key,'mode':'replace','release':'E','description':'A sustained original historical essay. Institutional sources provide contextual grounding; interpretive claims have not received line-by-line scholarly verification.','kicker':'EXTENDED HISTORICAL ESSAY','sourceStatus':registry[key]['sourceStatus'],'sources':registry[key]['sources'],'blocks':blocks}
        records.append(r);stats[key]={'words':count,'passages':len(blocks)}
    if set(registry)!=used:raise ValueError('Unused or missing provenance keys')
    DEST.write_text(''.join(json.dumps(r,ensure_ascii=False,separators=(',',':'))+'\n' for r in records),encoding='utf8')
    return stats
if __name__=='__main__':
    try:print(json.dumps(run(),indent=2))
    except (ValueError,OSError) as exc:print('Preparation failed:',exc,file=sys.stderr);sys.exit(1)
