#!/usr/bin/env python3
"""Identify real author figures for new arXiv papers.

This is intentionally *not* an automated analysis of the method. It records
figure numbers/captions from arXiv HTML only and supplies cautious Korean
reading prompts. A source-first pipeline later downloads the exact images.
Never invent Figure numbers, figures, metrics, or paper-specific conclusions.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import date, timedelta
from pathlib import Path

from extract_paper_figures import parse_html_figures

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'data/figure_catalog.json'
PAPERS = ROOT / 'data/papers.json'


def role_from_caption(caption: str, default: str) -> str:
    s = caption.lower()
    if re.search(r'\b(accuracy|performance|evaluat\w*|experiment\w*|benchmark\w*|success rate|comparison|ablation)\b', s):
        return 'findings'
    if re.search(r'\b(pipeline|framework|architecture|training|method|approach|model overview|policy overview)\b', s):
        return 'method'
    if re.search(r'\b(motivation|challenge|limitation|existing method|previous work)\b', s):
        return 'problem'
    return default


def choose(entries: dict) -> list[tuple[int, dict, str]]:
    """One motivation/method figure and one method/result figure if present."""
    ranked=[]
    for num, entry in entries.items():
        role=role_from_caption(entry.get('caption',''), 'idea' if num == 1 else 'method')
        # Select architecture before a generic illustration; experiment next.
        priority={'method':0,'findings':1,'idea':2,'problem':3}[role]
        ranked.append((priority,num,entry,role))
    ranked.sort()
    if not ranked:
        return []
    primary=ranked[0]
    secondary=next((x for x in ranked[1:] if x[3]=='findings' and primary[3]!='findings'), None)
    if not secondary:
        secondary=next((x for x in ranked[1:] if x[3]!='method' and primary[3]=='method'),None)
    if not secondary: secondary=ranked[1] if len(ranked)>1 else None
    chosen=[primary]+([secondary] if secondary else [])
    return [(n,e,r) for _,n,e,r in sorted(chosen,key=lambda x:x[1])]


def synthesize_entry(title: str, figures: list[tuple[int, dict, str]]) -> dict:
    info=[]
    for number,rec,section in figures:
        caption=str(rec.get('caption','')).strip()
        # Use the *source caption*, not a model guess, to name the figure.
        heading=caption.split(':',1)[-1].strip()
        if len(heading)>135: heading=heading[:132].rsplit(' ',1)[0]+'…'
        info.append({
            'number':number,
            'placement':section,
            'reading_title':heading or f'원논문 Figure {number}',
            'context':f'이 Figure는 저자가 논문에 넣은 실제 그림입니다. 아래 영어 원문 캡션과 본문 해당 부분을 함께 확인하세요. 현재 한국어 자동 미리보기 단계이므로 구조·수치에 관한 단정적인 해석은 보류합니다.',
            'steps':[
                '입력 정보, 중간 표현, 예측/제어 출력이 실제로 구분되어 표시되는지 확인합니다.',
                '그림이 모델 구조라면 화살표가 가리키는 데이터 흐름과 훈련·추론 시 사용 여부를 차례로 읽습니다.' if section=='method' else '그래프/사례 그림이라면 실험 조건, 비교 기준, 표시된 지표를 먼저 확인합니다.',
                '표·그래프 수치를 다른 논문과 비교하기 전에 데이터셋·평가 방식·로봇 구성이 같은지 확인합니다.'
            ],
            'locator':f'원문 Figure {number} / arXiv 원문 HTML'
        })
    return {
        'heading':f'{title} — 저자 원본 그림',
        'intro':'초록 기반으로 수집된 연구입니다. 첨부 Figure는 arXiv HTML에서 번호·캡션이 검증된 저자 원본만 사용합니다. 저자 설명을 확인하지 않고 상세 결과를 추정하지 않습니다.',
        'figures':info,
        'origin':'automatic-source-caption'
    }


def register(max_new: int = 16, days: int = 21):
    import requests
    papers=json.loads(PAPERS.read_text(encoding='utf-8'))['papers']
    existing=json.loads(CATALOG.read_text(encoding='utf-8'))
    cutoff=(date.today()-timedelta(days=days)).isoformat()
    session=requests.Session()
    added=0
    # Older curated entries already have manually authored figure-reading guides.
    # New automated papers get *only* source-caption-based provisional guides.
    for paper in papers:
        pid=str(paper['id'])
        if pid in existing or paper.get('curated') or paper.get('published','')<cutoff:
            continue
        if not re.fullmatch(r'\d{4}\.\d{4,5}',pid):continue
        if added>=max_new:break
        try:
            found=parse_html_figures(session,pid)
            chosen=choose(found)
            if not chosen:
                print(f'[SKIP] No verifiable arXiv HTML figure for {pid}')
                continue
            existing[pid]=synthesize_entry(paper['title'],chosen)
            added+=1
            print(f'[FIGURES] {pid}: '+', '.join(str(n) for n,_,_ in chosen),flush=True)
        except Exception as exc:
            print(f'[WARN] {pid}: figure discovery failed ({type(exc).__name__})',flush=True)
    if added:
        CATALOG.write_text(json.dumps(existing,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'[DONE] catalogued {added} new source-verified paper figure sets')
    return added


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--max-new',type=int,default=16)
    parser.add_argument('--days',type=int,default=21)
    args=parser.parse_args()
    register(args.max_new,args.days)
