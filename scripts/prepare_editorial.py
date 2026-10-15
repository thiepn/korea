#!/usr/bin/env python3
"""Compile a human-authored editorial Markdown volume into immutable KOREA import events.

`## <canonical ID>` opens a subject; `### <passage title>` opens a new passage.
Every prose paragraph under a passage becomes the paragraph text without padding.
The prepared JSONL is replay-safe through scripts/ingest.py and reviewable in git.
"""
from __future__ import annotations
import argparse,json,re,sys
from pathlib import Path
from build_corpus import canonical, DATA

ROOT=Path(__file__).resolve().parents[1]
def prepare(source:Path,target:Path,dry_run=False):
    titles=canonical(); items=[];current=None;block=None;outside=True
    for n,raw in enumerate(source.read_text(encoding='utf-8').splitlines(),1):
        line=raw.strip()
        if line.startswith('## ') and not line.startswith('### '):
            key=line[3:].strip()
            if key not in titles:raise ValueError(f'line {n}: unknown canonical ID {key}')
            if any(v['id']==key for v in items):raise ValueError(f'line {n}: duplicate ID {key}')
            current={'id':key,'mode':'replace','description':'An editorial introduction to '+titles[key]+', part of the expanding KOREA history archive.','kicker':'EXTENDED HISTORICAL ARCHIVE','release':'C','blocks':[]}
            items.append(current);block=None;outside=False
        elif line.startswith('### '):
            if outside or current is None:raise ValueError(f'line {n}: passage has no canonical article')
            title=line[4:].strip()
            if len(title)<5:raise ValueError(f'line {n}: inadequate passage title')
            block={'title':title,'paragraphs':[]};current['blocks'].append(block)
        elif line and not line.startswith('#'):
            if outside:continue
            if block is None:raise ValueError(f'line {n}: prose without passage')
            if len(re.findall(r'\b[\w’\'-]+\b',line))<40:raise ValueError(f'line {n}: passage too brief; no filler permitted')
            block['paragraphs'].append(line)
    if not items:raise ValueError('Volume contains no canonical subjects')
    for a in items:
        if len(a['blocks'])<3 or any(not b['paragraphs'] for b in a['blocks']):
            raise ValueError(f'{a["id"]}: expected at least three independently written passages')
        if (DATA/'articles'/f'{a["id"]}.json').exists():
            raise ValueError(f'{a["id"]}: already published. Use an explicit append source, never replace.')
    data=''.join(json.dumps(a,ensure_ascii=False,separators=(',',':'))+'\n' for a in items)
    if not dry_run:
        target.parent.mkdir(parents=True,exist_ok=True);target.write_text(data,encoding='utf-8')
    return {'subjects':len(items),'passages':sum(len(a['blocks']) for a in items),'editorial_words':sum(len(re.findall(r'\b[\w’\'-]+\b',p)) for a in items for b in a['blocks'] for p in b['paragraphs']),'bytes':len(data.encode('utf-8'))}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('output',type=Path);ap.add_argument('--dry-run',action='store_true');a=ap.parse_args()
    try:print(json.dumps(prepare(a.source,a.output,a.dry_run),indent=2))
    except ValueError as e:print('PREPARE FAILED:',e,file=sys.stderr);sys.exit(1)
