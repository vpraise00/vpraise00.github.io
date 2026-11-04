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

def post_page(p: dict, categories: dict) -> str:
    cat = categories.get(p.get('primary_category',''), {'label':'Research','color':'#7f9992'})
    name, id = str(p['title']), clean_slug(p['id'])
    date = str(p.get('published',''))
    summary = str(p.get('summary_ko',''))
    authors = ', '.join(map(str,p.get('authors', [])))
    review = p.get('review') or {}
    featured = bool(p.get('featured'))
    source_scope = '초록 + 공식 자료 기반 편집 해설' if p.get('curated') else ('AI 보조 분석 · 논문 PDF 기반 (검증 권장)' if review.get('source_scope')=='pdf+abstract' else '자동 수집 · 초록 기반 요약 (본문 검증 전)')
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
    sections=[]
    for index,(key,title,subtitle) in enumerate(LABELS,1):
        content=review.get(key) or '자료에서 이 항목을 별도로 확인할 수 없습니다. 원문을 참고해 주세요.'
        inner = f'<div class="evidence-box"><span>✳</span><p>{rich(content)}</p></div>' if key=='findings' else f'<p>{rich(content)}</p>'
        sections.append(f'<section class="article-section" id="{key}"><span class="section-number">0{index} / {h(subtitle).upper()}</span><h2>{h(title)}</h2>{inner}</section>')
    questions = ''.join(f'<li><span class="question-icon">?</span><span>{h(q)}</span><button type="button" class="ask-question" data-question="{h(q,quote=True)}">GPT에게 묻기 ↗</button></li>' for q in review.get('questions',[])[:6])
    if not questions: questions='<li>이 논문의 평가 프로토콜과 실제 배치 성능은 얼마나 일치할까?</li>'
    abstract = p.get('abstract','')
    pub_year = date[:4]
    tags=''.join(f'<span>#{h(t)}</span>' for t in p.get('tags',[]))
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
<section class="article-section" id="abstract"><span class="section-number">07 / ABSTRACT &amp; PROVENANCE</span><h2>원문 / 출처 확인</h2><div class="article-abstract"><p>{h(abstract)}</p></div><p style="font-size:11px;color:var(--muted);margin-top:13px">해설은 논문 저자들의 진술과 편집자의 비판적 질문을 구분합니다. 특정 지표·인과관계·재현성을 판단할 때는 반드시 <a style="color:var(--brand);text-decoration:underline" href="{source_url}" target="_blank" rel="noopener noreferrer">원문</a>의 실험 설정을 확인해 주세요.</p></section>
<section class="article-section"><span class="section-number">08 / TOPIC TAGS</span><h2>연구 키워드</h2><div class="article-tags">{tags}</div></section>
<div class="article-bottom-nav"><a href="../">← 모든 논문으로 돌아가기</a><a href="{source_url}" target="_blank" rel="noopener noreferrer">원문 읽기 ↗</a></div>
</article>
<aside class="article-side" aria-label="읽기 도우미"><div class="side-box"><h3>◈ RESEARCH COMPANION</h3><span class="subhead">논문 내용이나 선택한 문장에 대해 ChatGPT에 바로 질문할 수 있습니다.</span><button type="button" class="ask-gpt-button" id="ask-gpt"><span>✳</span> Ask ChatGPT about this paper ↗</button><button type="button" class="copy-prompt" id="copy-gpt">질문 내용 복사하기</button></div>
<div class="side-box"><h3>↗ ORIGINAL SOURCES</h3>{source_links}</div>
<div class="side-box"><h3>✎ PRIVATE RESEARCH NOTES</h3><span class="subhead">메모는 내 브라우저에만 저장됩니다. 자동 저장됩니다.</span><textarea id="paper-note" class="note-area" placeholder="이 논문의 아이디어, 재현할 실험, 후속 질문을 기록하세요..."></textarea><div class="note-status" id="note-status">메모 준비됨</div><div style="margin-top:11px"><select class="sort-select" id="custom-paper-category" style="max-width:100%;width:100%"><option value="">+ 내 분류에 추가</option></select></div></div>
<div class="side-box"><h3>✳ MY HIGHLIGHTS <span id="highlight-count" style="color:var(--muted);font-weight:500">0</span></h3><span class="subhead">본문에서 문장을 선택하면 표시하고 GPT에 질문할 수 있습니다.</span><div id="highlights-list" class="highlight-empty">선택해 저장한 문장이 이곳에 표시됩니다.</div></div>
<div class="side-box side-digest"><h3>READING METADATA</h3><span>INDEX DATE</span><strong>{h(date)}</strong><span>PAPER ID</span><strong>arXiv:{h(id)}</strong><span>REVIEW STATUS</span><strong>{'Editorial · evidence-linked' if p.get('curated') else ('AI-assisted · verify source' if review.get('generated_by')=='openai' else 'Abstract · metadata only')}</strong></div>
</aside></div></div></div>
<div id="selection-toolbar" class="selection-toolbar hidden"><button id="selection-save">✎ 하이라이트 저장</button><button id="selection-ask">✳ GPT에 질문</button></div><div class="toast hidden" id="toast" role="status"></div>
</body></html>'''

def build():
    content = json.loads((ROOT/'data/papers.json').read_text(encoding='utf-8'))
    config = json.loads((ROOT/'config/topics.json').read_text(encoding='utf-8'))
    papers=sorted(content.get('papers',[]),key=lambda p:(p.get('published',''),p.get('id','')),reverse=True)
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
    (ROOT/'data/papers.json').write_text(json.dumps({'last_checked':content.get('last_checked',''), 'papers':papers},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    stamp=content.get('last_checked','')[:10] or datetime.now(timezone.utc).date().isoformat()
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
