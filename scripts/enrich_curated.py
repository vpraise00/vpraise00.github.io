#!/usr/bin/env python3
"""Apply manually reviewed, evidence-separated technical deep dives to curated articles.

Run after seed_content.py if regenerating the initial curated catalogue:
    python scripts/enrich_curated.py
    python scripts/build_site.py
Never touches new automatically imported articles.
"""
from __future__ import annotations
import json
from pathlib import Path
from deep_content import D

ROOT = Path(__file__).resolve().parents[1]

SOURCE_LINKS = {
 '2610.40026': {'code_url': 'https://github.com/PrimitiveX/RoboSeed'},
 '2610.07922': {'project_url': 'https://openwam.stanford.edu/'},
 '2609.23578': {'project_url': 'https://ar-wam.github.io/', 'code_url': 'https://github.com/AR-WAM/AR-WAM'},
 '2609.16074': {'project_url': 'https://rcl-robotics.github.io/Awesome-World-Action-Models/'},
 '2504.16054': {'project_url': 'https://www.pi.website/blog/pi05'},
 '2403.12945': {'project_url': 'https://droid-dataset.github.io/'},
}

def apply() -> int:
    source=ROOT/'data/papers.json'
    data=json.loads(source.read_text(encoding='utf-8'))
    changed=0
    for paper in data['papers']:
        if not paper.get('curated') or paper['id'] not in D:
            continue
        original=D[paper['id']]
        deep=dict(original)
        # Authoring uses concise tuples; publish normalized dictionaries for the HTML renderer.
        columns={
            'pipeline': ('title','detail','io'),
            'mechanisms': ('title','body','watch'),
            'evidence': ('metric','value','context'),
        }
        for field,names in columns.items():
            deep[field]=[dict(zip(names,row)) if isinstance(row,(list,tuple)) else row
                         for row in original.get(field,[])]
        paper['deep_dive']=deep
        paper.update(SOURCE_LINKS.get(paper['id'],{}))
        # Reading time is an estimate based on Korean character count; not invented analysis duration.
        length=len(paper.get('summary_ko',''))+sum(len(str(v)) for v in paper.get('review',{}).values())
        length+=len(json.dumps(deep,ensure_ascii=False))
        paper['reading_minutes']=min(28,max(12,round(length/300)))
        changed+=1
    source.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Enriched {changed} curated posts with per-paper research deep dives.')
    return changed

if __name__=='__main__':
    apply()
