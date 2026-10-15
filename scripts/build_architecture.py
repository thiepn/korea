#!/usr/bin/env python3
"""Lossless canonical ID/title extraction; no historical reclassification or generated section titles."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent.parent
roman=['I','II','III','IV','V','VI','VII','VIII','IX','X']
parts=[]; count=0
for n in roman:
    source=ROOT/f'canonical/PART_{n}_ARCHITECTURE.md'
    s=source.read_text(encoding='utf-8')
    title=re.search(r'^part_title: "(.+)"$',s,re.M).group(1)
    period=re.search(r'\*\*Canonical period:\*\* (.+?)  ?$',s,re.M).group(1).strip()
    description=re.search(r'^## Part entry boundary\n(.+)',s,re.M)
    headings=list(re.finditer(r'^# Chapter ([IVX]+\.\d+) — (.+)$|^## ([IVX]+\.\d+\.\d+) — (.+)$',s,re.M))
    part={'id':n,'title':title,'period':period,'description':description.group(1).strip() if description else '', 'chapters':[]}
    chapter=None
    for j,m in enumerate(headings):
        if m.group(1):
            chapter={'id':m.group(1),'title':m.group(2),'subchapters':[]}
            part['chapters'].append(chapter)
        else:
            block=s[m.end():headings[j+1].start() if j+1<len(headings) else len(s)]
            related=re.search(r'\*\*Related units:\*\* (.+?)\s*$',block,re.M)
            risk=re.search(r'Historiographical risk \*\*(.+?)\*\*',block)
            chapter['subchapters'].append({'id':m.group(3),'title':m.group(4).strip(), 'related':re.findall(r'`([IVX]+\.\d+\.\d+)`',related.group(1)) if related else [],'risk':risk.group(1) if risk else 'Unspecified'})
            count+=1
    assert len(part['chapters'])==10,(n,'chapters')
    for ch in part['chapters']: assert len(ch['subchapters'])==10,(ch['id'],'subs')
    parts.append(part)
assert count==1000
(ROOT/'data/architecture.json').write_text(json.dumps({'sourceVersion':'MASTER v1.1','parts':parts,'counts':{'parts':10,'chapters':100,'subchapters':1000,'plannedSections':10000,'plannedTerminalSubsections':100000},'source':'Unmodified canonical Part architecture markdown files'},ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print('Built',len(parts),'Parts, 100 Chapters,',count,'Subchapters')
