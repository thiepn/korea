#!/usr/bin/env python3
"""Validate and import canonical KOREA content from JSONL batches, atomically per article.

Schema: {"id":"VI.4.2", "mode":"append"|"replace", "blocks":[
  {"title":"...", "paragraphs":["..."]}]}
Append is replay-safe: exact previously appended block sequence skips; overlapping but
nonidentical content is rejected. Existing canonical ID, title, and original passages
are never renumbered. `replace` is permitted ONLY for a currently unpublished ID.
`--dry-run` makes no changes. The compiler is a separate deliberate publish step.
"""
from __future__ import annotations
import argparse,json,hashlib,sys
from pathlib import Path
from build_corpus import DATA,canonical

def run(path:Path,dry_run=False):
    allowed=canonical(); plans={}; changes=[]
    for n,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
        if not line.strip():continue
        try: record=json.loads(line)
        except json.JSONDecodeError as exc:raise ValueError(f'line {n}: invalid JSON: {exc}') from exc
        key=record.get('id');mode=record.get('mode','append')
        if key not in allowed:raise ValueError(f'line {n}: unknown canonical ID {key}')
        if mode not in ('append','replace'):raise ValueError(f'line {n}: unsupported mode')
        blocks=record.get('blocks')
        if not isinstance(blocks,list) or not blocks or len(blocks)>100:
            raise ValueError(f'line {n}: expected 1–100 passage blocks')
        if any(not isinstance(b,dict) or not isinstance(b.get('title'),str) or not b['title'].strip() or not isinstance(b.get('paragraphs'),list) or not b['paragraphs'] or any(not isinstance(p,str) or len(p.strip())<20 for p in b['paragraphs']) for b in blocks):
            raise ValueError(f'line {n}: passage title/paragraph validation failed')
        if key in plans:raise ValueError(f'line {n}: duplicate ID in batch: {key}')
        target=DATA/'articles'/f'{key}.json'
        existing=json.loads(target.read_text(encoding='utf-8')) if target.exists() else None
        sources=record.get('sources',[])
        if sources:
            if not isinstance(sources,list) or len(sources)>12 or any(not isinstance(s,dict) or not all(isinstance(s.get(field),str) and s[field].strip() for field in ('institution','title','url','role')) or not s['url'].startswith('https://') for s in sources):
                raise ValueError(f'line {n}: invalid institutional source metadata')
        if record.get('sourceStatus') and (not isinstance(record['sourceStatus'],str) or len(record['sourceStatus'])>250):
            raise ValueError(f'line {n}: invalid editorial source status')
        for block in blocks:
            evidence=block.get('evidence',[])
            if not isinstance(evidence,list) or len(evidence)>8:raise ValueError(f'line {n}: invalid passage evidence list')
            for item in evidence:
                if not isinstance(item,dict) or not isinstance(item.get('claim'),str) or len(item['claim'])<24 or not isinstance(item.get('locator'),str) or len(item['locator'])<12 or item.get('type') not in ('direct','context') or not isinstance(item.get('sourceIndex'),int) or not 0<=item['sourceIndex']<len(sources):
                    raise ValueError(f'line {n}: invalid or ungrounded evidence reference')
        base=(existing.copy() if existing else {'id':key,'title':allowed[key],'kicker':record.get('kicker','HISTORY'), 'description':record.get('description',''), 'release':record.get('release',''), 'sourceStatus':record.get('sourceStatus','Unverified editorial narrative'), 'sources':sources, 'blocks':[]})
        if base['title']!=allowed[key]:raise ValueError(f'line {n}: existing title diverges from canonical')
        already=[{'title':b['title'],'paragraphs':b['paragraphs'],'evidence':b.get('evidence',[])} for b in base['blocks']]
        incoming=[{'title':b['title'].strip(),'paragraphs':[p.strip() for p in b['paragraphs']],'evidence':b.get('evidence',[])} for b in blocks]
        if incoming and len(already)>=len(incoming) and already[-len(incoming):]==incoming:
            changes.append({'id':key,'status':'unchanged (idempotent replay)'})
            continue
        if existing and mode=='replace':raise ValueError(f'line {n}: cannot replace published article {key}')
        if any(x in already for x in incoming):raise ValueError(f'line {n}: overlapping passage content, refusing ambiguous append')
        if len(already)+len(incoming)>999:raise ValueError(f'line {n}: excessive passage count (maximum 999)')
        for i,b in enumerate(incoming,len(already)+1):
            base['blocks'].append({'id':f'{key}:b{i:02d}','title':b['title'],'paragraphs':b['paragraphs'],'label':'Editorial synthesis · selected evidence anchors','sequence':i,**({'evidence':b['evidence']} if b['evidence'] else {})})
        plans[target]=base;changes.append({'id':key,'status':'will import','passages':len(incoming)})
    if not dry_run:
        # All validation occurs before any source mutation. Temp + replace keeps each JSON intact.
        for target,body in plans.items():
            text=json.dumps(body,ensure_ascii=False,indent=2)+'\n'
            temp=target.with_suffix('.json.tmp');temp.write_text(text,encoding='utf-8');temp.replace(target)
    return {'dry_run':dry_run,'articles_updated':len(plans),'events':changes}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('path',type=Path);p.add_argument('--dry-run',action='store_true');opts=p.parse_args()
    try: print(json.dumps(run(opts.path,opts.dry_run),ensure_ascii=False,indent=2))
    except (ValueError,OSError) as exc:print('INGEST FAILED:',exc,file=sys.stderr);sys.exit(1)
