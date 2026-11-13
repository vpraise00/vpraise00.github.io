#!/usr/bin/env python3
"""Build static paper posts, RSS and sitemap. No runtime backend required."""
from __future__ import annotations
import json
import re
from pathlib import Path
from html import escape as h
from urllib.parse import quote
from xml.sax.saxutils import escape as xml_escape
from datetime import datetime, timezone
from functools import lru_cache

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = 'https://vpraise00.github.io/'
PAPERS = ROOT / 'papers'
LABELS = [
 ('problem', '연구가 풀려는 문제', '문제 정의'),
 ('idea', '핵심 아이디어', '핵심 기여'),
 ('method', '방법론 · 아키텍처', '설계와 학습'),
 ('findings', '실험과 주요 발견', '근거와 결과'),
 ('limitations', '한계와 비판적 검토', '비판적 해석'),
]

def clean_slug(x: str) -> str:
    if not re.fullmatch(r'\d{4}\.\d{4,5}(?:v\d+)?', x):
        raise ValueError(f'Invalid arXiv identifier: {x!r}')
    return x

def post_path(p: dict) -> str:
    return f'papers/{clean_slug(p["id"])}.html'

def rich(s: str) -> str:
    safe = h(str(s))
    return re.sub(r'\*\*(.*?)\*\*',r'<strong>\1</strong>',safe)

def render_deep_dive(p: dict) -> tuple[str, str]:
    """Rich structured commentary with source/analyst boundaries. Escapes all inputs."""
    d=p.get('deep_dive') or (p.get('review') or {}).get('deep_dive') or {}
    if not isinstance(d,dict) or not d:
        return '', ''
    toc=''
    parts=[]
    def para(text):
        return '<p>'+rich(text)+'</p>'
    def item(text):
        return '<li>'+rich(text)+'</li>'
    lead=str(d.get('lead',''))
    if lead:
        parts.append('<section class="deep-intro"><div class="deep-heading"><span>⌁ DEEP TECHNICAL REVIEW</span><b>연구자용 상세 해설</b></div>'+para(lead)+'</section>')
    steps=d.get('pipeline') or []
    if steps:
        toc+='<a href="#pipeline">모델 구조와 처리 흐름</a>'
        cards=''.join('<li class="pipeline-step"><span class="pipeline-num">'+f'{i:02d}'+'</span><div><h3>'+h(s.get('title',''))+'</h3>'+para(s.get('detail',''))+('<span class="pipeline-io">'+h(s.get('io',''))+'</span>' if s.get('io') else '')+'</div></li>' for i,s in enumerate(steps[:7],1) if isinstance(s,dict))
        parts.append('<section class="article-section deep-section" id="pipeline"><span class="section-number">DEEP DIVE / 01</span><h2>모델 구조와 처리 흐름</h2><p class="deep-section-help">개념적 처리 순서를 정리한 편집 다이어그램이며 원논문의 그림을 복제한 것은 아닙니다.</p><ol class="pipeline-list">'+cards+'</ol></section>')
    notes=d.get('mechanisms') or []
    if notes:
        toc+='<a href="#mechanisms">알고리즘·학습 신호</a>'
        cards=''.join('<div class="mechanism-card"><h3>'+h(n.get('title',''))+'</h3>'+para(n.get('body',''))+('<div class="mechanism-why"><b>읽기 포인트</b>'+rich(n.get('watch',''))+'</div>' if n.get('watch') else '')+'</div>' for n in notes[:8] if isinstance(n,dict))
        parts.append('<section class="article-section deep-section" id="mechanisms"><span class="section-number">DEEP DIVE / 02</span><h2>핵심 설계·학습 신호 해설</h2><div class="mechanism-grid">'+cards+'</div></section>')
    results=d.get('evidence') or []
    if results:
        toc+='<a href="#evidence">실험·성능 근거표</a>'
        rows=''.join('<tr><td>'+h(r.get('metric',''))+'</td><td class="measure">'+h(r.get('value',''))+'</td><td>'+rich(r.get('context',''))+'</td></tr>' for r in results[:9] if isinstance(r,dict))
        notes=h(d.get('evidence_note','해당 수치는 논문 저자들의 보고이며 서로 다른 데이터셋·설정의 수치는 직접 비교하면 안 됩니다.'))
        parts.append('<section class="article-section deep-section" id="evidence"><span class="section-number">DEEP DIVE / 03</span><h2>실험 결과를 제대로 읽기</h2><div class="table-scroll"><table class="evidence-table"><thead><tr><th>평가 항목</th><th>보고된 결과</th><th>해석 / 실험 조건</th></tr></thead><tbody>'+rows+'</tbody></table></div><p class="evidence-note">ⓘ '+notes+'</p></section>')
    compared=d.get('comparison') or ''
    if compared:
        toc+='<a href="#comparison">베이스라인과 차이</a>'
        parts.append('<section class="article-section deep-section" id="comparison"><span class="section-number">DEEP DIVE / 04</span><h2>기존 연구와 무엇이 다른가?</h2><div class="comparison-panel">'+para(compared)+'</div></section>')
    check=d.get('reading_guide') or []
    if check:
        toc+='<a href="#reading-guide">논문 정독 체크리스트</a>'
        parts.append('<section class="article-section deep-section" id="reading-guide"><span class="section-number">DEEP DIVE / 05</span><h2>원문을 읽으면서 확인할 4가지</h2><ol class="reading-list">'+''.join(item(x) for x in check[:6])+'</ol></section>')
    rep=d.get('replication') or {}
    if isinstance(rep,dict) and rep:
        toc+='<a href="#replication">재현·후속 연구 설계</a>'
        fields=[('hypothesis','검증 가설'),('setup','구체적 실험 설계'),('baselines','비교군·Ablation'),('metrics','기록할 지표'),('risks','실패 해석·주의점')]
        text=''.join('<div class="replication-row"><strong>'+h(label)+'</strong>'+para(rep[key])+'</div>' for key,label in fields if rep.get(key))
        parts.append('<section class="article-section deep-section" id="replication"><span class="section-number">RESEARCH LAB / EDITORIAL PROPOSAL</span><h2>내 연구에 적용한다면?</h2><p class="proposal-disclaimer">아래는 논문 저자의 검증 결과가 아니라, 논문에서 출발해 설계한 **후속 실험 제안**입니다.</p><div class="replication-grid">'+text+'</div></section>')
    neighbors=d.get('related') or []
    if neighbors:
        toc+='<a href="#related">연결해서 읽기</a>'
        lis=[]
        for target in neighbors[:4]:
            try: valid=clean_slug(str(target))
            except ValueError: continue
            lis.append(f'<a href="{valid}.html">arXiv:{h(valid)} <span>관련 포스팅 보기 ↗</span></a>')
        if lis: parts.append('<section class="article-section deep-section" id="related"><span class="section-number">RESEARCH MAP</span><h2>연결해서 읽을 논문</h2><div class="related-papers">'+''.join(lis)+'</div></section>')
    return toc, ''.join(parts)

@lru_cache(maxsize=1)
def figure_catalog():
    path=ROOT/'data/figure_catalog.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}

@lru_cache(maxsize=1)
def figure_status():
    path=ROOT/'data/figure_extract_status.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}

def clip_original_caption(value, max_words=22):
    """Show only a *short* original caption excerpt (not full copyrighted text)."""
    words=str(value).split()
    return ' '.join(words[:max_words])+('…' if len(words)>max_words else '')

# Figure placements are editorial decisions about WHEN the reader needs a source
# figure; they are not inferred from the figure number. Figures remain unmodified
# original author material, with the provenance recorded in figure_extract_status.
FIGURE_PLACEMENTS = {
    '2610.42021': {1:'idea',2:'method'},      # Nexus-VLA
    '2610.40373': {1:'problem',2:'method'},   # HiFOR
    '2610.40026': {1:'method',2:'findings'},  # RoboSeed
    '2610.07922': {1:'idea',2:'method'},      # OpenWAM
    '2609.23578': {1:'idea',2:'findings'},    # AR-WAM
    '2609.19600': {1:'idea',2:'method'},     # WorldContact
    '2609.16074': {1:'idea',2:'comparison'}, # survey
    '2608.01397': {1:'idea',2:'method'},
    '2610.22146': {1:'method',2:'findings'},     # SG-WAM
    '2605.00080': {1:'idea',2:'comparison'}, # survey
    '2504.16054': {2:'findings',3:'method'}, # pi0.5: deployment example; training recipe
    '2503.14734': {1:'idea',2:'method'},     # GR00T
    '2502.05855': {1:'method',2:'findings'}, # DexVLA
    '2410.24164': {2:'findings',3:'method'}, # pi0: application; architecture
    '2406.09246': {1:'idea',2:'method'},     # OpenVLA
    '2405.12213': {1:'idea',2:'findings'},   # Octo
    '2403.12945': {1:'problem',2:'findings'} # DROID
}

def render_visual_figures(p: dict) -> dict[str, str]:
    """Render *original* author figures at their pedagogical section, never as a gallery.

    The paper-specific figure placement map routes architectures into the method,
    real-world demonstrations and evaluation plots into findings, and motivation
    contrasts into problem/idea. No figure is moved into the page introduction.
    """
    pid=str(p['id']); guide=figure_catalog().get(pid)
    if not guide: return {}
    available=figure_status().get(pid,{})
    source=f'https://arxiv.org/abs/{pid}'
    placements=FIGURE_PLACEMENTS.get(pid,{})
    grouped={}
    for index,fig in enumerate(guide.get('figures',[]),1):
        n=int(fig['number']);display_n=int(fig.get('display_number',n));record=available.get(str(n)) or {}
        path=record.get('local','')
        # Source-reviewed author-project figures can be linked directly; never trust
        # arbitrary remote URLs from metadata as executable/embedded markup.
        remote=str(record.get('remote_url') or '')
        author_remote=bool(
          (pid == '2611.04527'
           and record.get('method') == 'author_project_exact_figure'
           and remote in {
             'https://harryjo97.github.io/dreamfree/assets/figures/method_v2.png?v=20261103',
             'https://harryjo97.github.io/dreamfree/assets/figures/droid_real_two_row.png'
           })
          or
          (pid == '2610.22146'
           and record.get('method') == 'arxiv_html_exact_figure'
           and remote in {
             'https://arxiv.org/html/2610.22146v2/sec/imgs/method.jpg',
             'https://arxiv.org/html/2610.22146v2/importance_metric.svg'
           })
        )
        image_exists=bool((path and (ROOT/path).exists()) or author_remote)
        if image_exists:
            img=(remote if author_remote else '../'+path)
            img=h(img,quote=True)
            method=record.get('method','')
            kind=(('arXiv HTML 저자 원본 (외부 링크)' if pid=='2610.22146' else '저자 공식 프로젝트 원본 (외부 링크)') if author_remote else ('arXiv HTML 저자 원본' if method=='arxiv_html_exact_figure' else '원논문 PDF 자동 추출 (크롭 검수 필요)'))
            source_link=h(record.get('source',source),quote=True)
            image='<div class="original-figure-stage"><a href="'+img+'" target="_blank" rel="noopener noreferrer" title="원문 그림 크게 보기"><img src="'+img+'" alt="'+h(p['title']+f' Figure {display_n} 원본',quote=True)+'" loading="lazy" decoding="async" referrerpolicy="no-referrer"/></a></div>'
            clip=clip_original_caption(fig.get('verified_caption') or record.get('caption',''))
            capt='<p class="original-caption"><strong>'+('편집 캡션 요약' if fig.get('verified_caption') else '원문 캡션 일부')+'</strong> '+h(clip)+'</p>' if clip else ''
            page=record.get('page');page_str=' · PDF p.'+str(page) if page else ''
        else:
            kind='원본 이미지 확인 대기 · 다른 이미지로 대체하지 않음'
            source_link=h(source,quote=True)
            image='<div class="original-figure-missing"><p>이 Figure의 원본 이미지가 아직 확보되지 않았습니다.</p><a href="https://arxiv.org/pdf/'+h(pid)+'" target="_blank" rel="noopener noreferrer">PDF에서 Figure '+str(display_n)+' 직접 보기 ↗</a></div>'
            capt='';page_str=''
        bullets=''.join('<li><span class="reading-step-number">'+f'{j:02d}'+'</span><p>'+rich(item)+'</p></li>' for j,item in enumerate(fig.get('steps',[])[:5],1))
        placement=fig.get('placement') or placements.get(n,'method')
        if placement not in {'problem','idea','method','findings','comparison','limitations'}: placement='method'
        context=rich(fig.get('context',''))
        block=''.join([
          '<figure class="original-paper-figure inline-source-figure" id="original-figure-'+str(n)+'">',
          '<div class="original-figure-header"><span class="source-figure-no">원논문 FIGURE '+str(display_n)+'</span><span class="figure-proof">'+h(kind)+'</span></div>',
          '<h3>'+h(fig.get('reading_title','원논문 그림으로 이해하기'))+'</h3>',
          '<p class="figure-context-bridge">'+context+'</p>',
          image,
          '<figcaption class="source-figure-caption">저자 원문 · arXiv:'+h(pid)+' · Figure '+str(display_n)+page_str+' · <a href="'+source_link+'" target="_blank" rel="noopener noreferrer">출처 확인 ↗</a></figcaption>',
          capt,
          '<div class="original-figure-explanation"><span class="figure-explainer-kicker">이 그림에서 꼭 확인할 것</span><ol>'+bullets+'</ol>',
          '<p class="figure-note-boundary">한국어 해설은 이해를 돕기 위한 편집 해석이며 저자 논문에서 검증된 수치나 그림의 모든 패널을 대체하지 않습니다.</p></div>',
          '</figure>'])
        grouped.setdefault(placement,[]).append(block)
    return {key:''.join(value) for key,value in grouped.items()}


def unpack_deep_sections(html: str) -> dict[str, str]:
    """Move existing deep-dive sections into their related narrative context."""
    fragments={}
    for m in re.finditer(r'<section class="(?:article-section deep-section|deep-intro)"(?: id="[^"]+")?>.*?</section>',html,re.S):
        segment=m.group(0)
        idmatch=re.search(r'<section[^>]* id="([^"]+)"',segment[:180])
        fragments[idmatch.group(1) if idmatch else 'intro']=segment
    return fragments

def post_page(p: dict, categories: dict) -> str:
    cat = categories.get(p.get('primary_category',''), {'label':'Research','color':'#7f9992'})
    name, id = str(p['title']), clean_slug(p['id'])
    date = str(p.get('published',''))
    summary = str(p.get('summary_ko',''))
    authors = ', '.join(map(str,p.get('authors', [])))
    review = p.get('review') or {}
    featured = bool(p.get('featured'))
    source_scope = str(p.get('source_scope_ko') or '원문 전체와 Figure·Table을 대조한 편집 해설 · 독립 재현은 별도') if p.get('editorial_verified') else '초록 + 공식 자료 기반 편집 해설' if p.get('curated') else ('AI 보조 분석 · 논문 PDF 기반 (검증 권장)' if review.get('source_scope')=='pdf+abstract' else '자동 수집 · 초록 기반 요약 (본문 검증 전)')
    article_data = json.dumps(p, ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    # Do not render untrusted paper-provided URL as a script/link; arxiv link is built from validated id.
    source_url = f'https://arxiv.org/abs/{id}'
    pdf_url = f'https://arxiv.org/pdf/{id}'
    source_links = f'<a class="side-resource" href="{source_url}" target="_blank" rel="noopener noreferrer"><span>arXiv 원문</span><b>↗</b></a><a class="side-resource" href="{pdf_url}" target="_blank" rel="noopener noreferrer"><span>논문 PDF</span><b>↗</b></a>'
    for field,label in [('project_url','프로젝트 페이지'),('code_url','코드 / 구현')]:
        url=str(p.get(field) or '')
        if url.startswith('https://') and not any(ch in url for ch in '<>"\''):
            source_links+=f'<a class="side-resource" href="{h(url,quote=True)}" target="_blank" rel="noopener noreferrer"><span>{label}</span><b>↗</b></a>'
    toc=''.join(f'<a href="#{key}">{h(title)}</a>' for key,title,_ in LABELS)
    toc+='<a href="#questions">다음 연구 질문</a><a href="#abstract">원문 · 출처</a>'
    # The deep-dive items are inserted into the TOC after baseline sections.

    deep_toc, deep_html = render_deep_dive(p)
    deep_parts=unpack_deep_sections(deep_html)
    figure_parts=render_visual_figures(p)
    sections=[]
    if deep_parts.get('intro'):
        sections.append(deep_parts['intro'])
    for index,(key,title,subtitle) in enumerate(LABELS,1):
        content=review.get(key) or '이 항목은 아직 초록 수준으로만 확인되었습니다. 상세 근거는 원문을 참고하세요.'
        inner = f'<div class="evidence-box"><span>✳</span><p>{rich(content)}</p></div>' if key=='findings' else f'<p>{rich(content)}</p>'
        sections.append(f'<section class="article-section" id="{key}"><span class="section-number">0{index} / {h(subtitle).upper()}</span><h2>{h(title)}</h2>{inner}</section>')
        # Introduce a source figure *after* the explanation that motivates it.
        if key == 'idea':
            sections.append(figure_parts.get('idea',''))
            sections.append(deep_parts.get('comparison',''))
        if key == 'method':
            # Step-by-step method FIRST; author architecture figure immediately after.
            sections.append(deep_parts.get('pipeline',''))
            sections.append(figure_parts.get('method',''))
            sections.append(deep_parts.get('mechanisms',''))
        elif key != 'idea':
            sections.append(figure_parts.get(key,''))
        if key == 'findings':
            sections.append(deep_parts.get('evidence',''))
        if key == 'limitations':
            sections.append(deep_parts.get('replication',''))
    # Source figure attached to comparison after the *comparison* explanation,
    # not in a picture-heavy introduction.
    if figure_parts.get('comparison'):
        comparator=deep_parts.get('comparison','')
        if comparator and comparator in sections:
            at=sections.index(comparator)+1
            sections.insert(at,figure_parts['comparison'])
        else:
            at=next((i+1 for i,x in enumerate(sections) if 'id="idea"' in x),2)
            sections.insert(at,figure_parts['comparison'])
    sections.extend([deep_parts.get('reading-guide',''),deep_parts.get('related','')])
    questions = ''.join(f'<li><span class="question-icon">?</span><span>{h(q)}</span><button type="button" class="ask-question" data-question="{h(q,quote=True)}">GPT에게 묻기 ↗</button></li>' for q in review.get('questions',[])[:6])
    if not questions: questions='<li>이 논문의 평가 프로토콜과 실제 배치 성능은 얼마나 일치할까?</li>'
    abstract = p.get('abstract','')
    pub_year = date[:4]
    tags=''.join(f'<span>#{h(t)}</span>' for t in p.get('tags',[]))
    toc_items=[('overview','핵심 한눈에'),('problem','문제 정의'),('idea','핵심 아이디어')]
    if deep_parts.get('comparison'): toc_items.append(('comparison','기존 연구와 차이'))
    toc_items.append(('method','방법론'))
    if deep_parts.get('pipeline'): toc_items.append(('pipeline','단계별 처리 흐름'))
    if deep_parts.get('mechanisms'): toc_items.append(('mechanisms','학습 신호·세부 구현'))
    toc_items.append(('findings','실험 결과'))
    if deep_parts.get('evidence'): toc_items.append(('evidence','성능·조건 비교표'))
    toc_items.append(('limitations','한계'))
    if deep_parts.get('replication'): toc_items.append(('replication','재현·후속 연구'))
    if deep_parts.get('reading-guide'): toc_items.append(('reading-guide','원문 정독 체크리스트'))
    if deep_parts.get('related'): toc_items.append(('related','연결해서 읽기'))
    toc_items.extend([('questions','남는 질문'),('abstract','원문·출처')])
    toc=''.join(f'<a href="#{key}">{h(label)}</a>' for key,label in toc_items)
    deep_mode = bool(deep_html)
    if deep_mode:
        # Existing summary sections remain useful, but research sections should be accessible right away.
        source_scope = source_scope + ' · 상세 연구 노트 포함' + (' · 원논문 Figure 문맥별 해설' if figure_parts else '')

    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="theme-color" content="#f6f7f5"/>
<title>{h(name)} | Embodied Research Radar</title>
<meta name="description" content="{h(summary, quote=True)}"/>
<meta property="og:title" content="{h(name,quote=True)}"/><meta property="og:description" content="{h(summary,quote=True)}"/>
<meta property="og:type" content="article"/><meta property="article:published_time" content="{h(date)}"/>
<link rel="canonical" href="{BASE_URL}{post_path(p)}"/>
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml"/>
<link rel="stylesheet" href="../assets/styles.css"/>
<script type="application/ld+json">{json.dumps({'@context':'https://schema.org','@type':'ScholarlyArticle','name':name,'datePublished':date,'author':[{'@type':'Person','name':a} for a in p.get('authors',[]) if a!='et al.'],'url':source_url,'isBasedOn':source_url},ensure_ascii=False).replace('<','\\u003c')}</script>
<script id="paper-data" type="application/json">{article_data}</script>
<script defer src="../assets/shared.js"></script><script defer src="../assets/paper.js"></script>
</head><body class="article-page"><div class="article-shell">
<header class="article-topbar"><a href="../" class="article-logo"><span class="article-logo-symbol">R</span> RESEARCH RADAR</a><div class="article-top-actions"><a href="../">← 모든 논문</a><button type="button" id="article-theme">◐</button><a href="https://github.com/vpraise00/vpraise00.github.io" target="_blank" rel="noopener noreferrer">GITHUB ↗</a></div></header>
<div class="article-progress"><div id="reading-progress"></div></div>
<div class="article-container"><div class="article-breadcrumb"><a href="../">DISCOVER</a><span>/</span><a href="../?category={quote(p.get('primary_category',''))}">{h(cat['label'])}</a><span>/</span><span>{h(pub_year)} RESEARCH</span></div>
<div class="article-hero"><div class="article-meta"><span class="cat-badge" style="--cat-color:{h(cat['color'])}">{h(cat['label'])}</span><span>{h(date)}</span><span>•</span><span>{int(p.get('reading_minutes',7))} min read</span>{'<span>•</span><span>✳ Curated</span>' if featured else ''}</div>
<h1 class="article-title">{h(name)}</h1><p class="article-lead">{h(summary)}</p><div class="article-author-row"><div class="article-byline"><span class="author-icon">◈</span><div><strong>{h(authors)}</strong><span>arXiv:{h(id)} · 논문 소개 / Korean research digest</span></div></div><div class="article-actions"><button type="button" class="save-button" id="save-paper">☆ 저장</button><button type="button" id="share-paper">↗ 공유</button></div></div></div>
<div class="article-columns"><article class="article-body" id="article-body"><div class="article-toc-inline"><strong>IN THIS DEEP DIVE</strong>{toc}</div>
<p class="source-scope">▧ {h(source_scope)}</p>
<section class="article-section" id="overview"><span class="section-number">00 / ONE-MINUTE RECAP</span><h2>핵심을 먼저 읽기</h2><p>{rich(review.get('one_line') or summary)}</p></section>
{''.join(sections)}
<section class="article-section" id="questions"><span class="section-number">06 / RESEARCH QUESTIONS</span><h2>읽고 나서 남는 질문</h2><ul class="question-list">{questions}</ul></section>
<section class="article-section" id="abstract"><span class="section-number">07 / ABSTRACT &amp; PROVENANCE</span><h2>원문 / 출처 확인</h2><p class="source-caveat">{'편집자가 작성한 초록 기반 한국어 요약이며 공식 영문 초록의 원문/번역이 아닙니다.' if p.get('curated') else 'arXiv에 등록된 초록을 자동 수집했습니다.'}</p><div class="article-abstract"><p>{h(abstract)}</p></div><p style="font-size:11px;color:var(--muted);margin-top:13px">해설은 논문 저자들의 진술과 편집자의 비판적 질문을 구분합니다. 특정 지표·인과관계·재현성을 판단할 때는 반드시 <a style="color:var(--brand);text-decoration:underline" href="{source_url}" target="_blank" rel="noopener noreferrer">원문</a>의 실험 설정을 확인해 주세요.</p></section>
<section class="article-section"><span class="section-number">08 / TOPIC TAGS</span><h2>연구 키워드</h2><div class="article-tags">{tags}</div></section>
<div class="article-bottom-nav"><a href="../">← 모든 논문으로 돌아가기</a><a href="{source_url}" target="_blank" rel="noopener noreferrer">원문 읽기 ↗</a></div>
</article>
<aside class="article-side" aria-label="읽기 도우미"><div class="side-box"><h3>◈ RESEARCH COMPANION</h3><span class="subhead">논문 내용이나 선택한 문장에 대해 ChatGPT에 바로 질문할 수 있습니다.</span><button type="button" class="ask-gpt-button" id="ask-gpt"><span>✳</span> Ask ChatGPT about this paper ↗</button><button type="button" class="copy-prompt" id="copy-gpt">질문 내용 복사하기</button></div>
<div class="side-box"><h3>↗ ORIGINAL SOURCES</h3>{source_links}</div>
<div class="side-box"><h3>✎ PRIVATE RESEARCH NOTES</h3><span class="subhead">메모는 내 브라우저에만 저장됩니다. 자동 저장됩니다.</span><textarea id="paper-note" class="note-area" placeholder="이 논문의 아이디어, 재현할 실험, 후속 질문을 기록하세요..."></textarea><div class="note-status" id="note-status">메모 준비됨</div><div style="margin-top:11px"><select class="sort-select" id="custom-paper-category" style="max-width:100%;width:100%"><option value="">+ 내 분류에 추가</option></select></div></div>
<div class="side-box"><h3>✳ MY HIGHLIGHTS <span id="highlight-count" style="color:var(--muted);font-weight:500">0</span></h3><span class="subhead">본문에서 문장을 선택하면 표시하고 GPT에 질문할 수 있습니다.</span><div id="highlights-list" class="highlight-empty">선택해 저장한 문장이 이곳에 표시됩니다.</div></div>
<div class="side-box side-digest"><h3>READING METADATA</h3><span>INDEX DATE</span><strong>{h(date)}</strong><span>PAPER ID</span><strong>arXiv:{h(id)}</strong><span>REVIEW STATUS</span><strong>{'Source-crosschecked editorial · replication not independently verified' if p.get('editorial_verified') else ('Editorial · verify' if p.get('curated') else 'Abstract · metadata only')}</strong></div>
</aside></div></div></div>
<div id="selection-toolbar" class="selection-toolbar hidden"><button id="selection-save">✎ 하이라이트 저장</button><button id="selection-ask">✳ GPT에 질문</button></div><div class="toast hidden" id="toast" role="status"></div>
</body></html>'''

def build():
    content = json.loads((ROOT/'data/papers.json').read_text(encoding='utf-8'))
    config = json.loads((ROOT/'config/topics.json').read_text(encoding='utf-8'))
    gate=json.loads((ROOT/'data/editorial_approvals.json').read_text(encoding='utf-8'))
    edits=json.loads((ROOT/'data/editorial_content.json').read_text(encoding='utf-8'))
    approved=set(gate.get('approved_ids',[]))
    # FAIL CLOSED: unapproved metadata stays archived, never becomes a published article.
    papers=sorted(({**p, **edits[p['id']]} for p in content.get('papers',[]) if p.get('id') in approved and p.get('id') in edits and edits[p['id']].get('editorial_verified') is True),key=lambda p:(p.get('published',''),p.get('id','')),reverse=True)
    ids=set()
    for p in papers:
        clean_slug(p['id'])
        if p['id'] in ids: raise ValueError(f'Duplicate arXiv ID: {p["id"]}')
        ids.add(p['id'])
    categories={v['id']:v for v in config['categories']}
    PAPERS.mkdir(exist_ok=True)
    for path in PAPERS.glob('*.html'):
        if path.stem not in ids: path.unlink()
    for p in papers:
        (ROOT/post_path(p)).write_text(post_page(p,categories),encoding='utf-8')
    # Order the saved data for browsing and diff stability.
    # Archive data/papers.json is intentionally never overwritten by the public site builder.
    stamp=max(content.get('last_checked','')[:10],gate.get('updated_at','')) or datetime.now(timezone.utc).date().isoformat()
    sitemap=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',f'<url><loc>{BASE_URL}</loc><lastmod>{h(stamp)}</lastmod></url>']
    for p in papers:sitemap.append(f'<url><loc>{BASE_URL}{post_path(p)}</loc><lastmod>{h(p.get("updated",p.get("published",""))[:10])}</lastmod></url>')
    sitemap.append('</urlset>')
    (ROOT/'sitemap.xml').write_text('\n'.join(sitemap)+'\n',encoding='utf-8')
    rows=[]
    for p in papers[:40]:
        rows.append(f'<item><title>{xml_escape(p["title"])}</title><link>{BASE_URL}{post_path(p)}</link><guid isPermaLink="true">{BASE_URL}{post_path(p)}</guid><description>{xml_escape(p.get("summary_ko", ""))}</description><category>{xml_escape(p.get("primary_category", ""))}</category></item>')
    (ROOT/'feed.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>Embodied Research Radar</title><link>'+BASE_URL+'</link><description>VLA, WAM, Robotics 연구 브리핑</description><language>ko</language>\n'+'\n'.join(rows)+'\n</channel></rss>\n',encoding='utf-8')
    (ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE_URL+'sitemap.xml\n',encoding='utf-8')
    print(f'Built {len(papers)} static research posts, sitemap and RSS feed.')

if __name__=='__main__':build()
