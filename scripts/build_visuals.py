#!/usr/bin/env python3
"""Render original, source-labeled SVG reading diagrams from visual_studies.json.
Do not put author figures in the repository: link author-hosted images with attribution.
"""
from __future__ import annotations
import json
from html import escape
from pathlib import Path
R=Path(__file__).resolve().parents[1]
O=R/'assets'/'figures'

def t(v): return escape(str(v),quote=True)
def svg_start(paper_id,fig,w=1180,h=470):
    title=fig['title']
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{t(title)}</title><desc id="desc">논문 독해를 돕기 위해 직접 제작한 개념도. 원논문 Figure가 아니며 원논문을 확인해야 합니다.</desc>
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#102831"/><stop offset="1" stop-color="#182e3e"/></linearGradient><linearGradient id="panel" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#22424a"/><stop offset="1" stop-color="#18333d"/></linearGradient><pattern id="dots" x="0" y="0" width="30" height="30" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#60999a" opacity=".15"/></pattern><marker id="arrow" viewBox="0 0 9 9" refX="7" refY="4.5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L9 4.5L0 9Z" fill="#84dbce"/></marker></defs>
<rect width="{w}" height="{h}" rx="20" fill="url(#bg)"/><rect width="{w}" height="{h}" rx="20" fill="url(#dots)"/><circle cx="1075" cy="35" r="250" fill="none" stroke="#4a9691" stroke-opacity=".13" stroke-width="1"/><circle cx="1080" cy="40" r="155" fill="none" stroke="#4a9691" stroke-opacity=".12" stroke-width="1"/>
<text x="50" y="49" font-family="Arial, sans-serif" font-size="11" font-weight="700" letter-spacing="3.5" fill="#65dac7">RESEARCH RADAR / FIGURE WALKTHROUGH</text><text x="1117" y="49" text-anchor="end" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#8aabb3">{t(paper_id)}</text>
<text x="49" y="96" font-family="NanumGothic, Noto Sans CJK KR, Malgun Gothic, Arial, sans-serif" font-size="29" font-weight="800" fill="#f0fffa">{t(title)}</text>
<text x="50" y="130" font-family="NanumGothic, Noto Sans CJK KR, Malgun Gothic, Arial, sans-serif" font-size="15" fill="#b6cdd1">{t(fig['subtitle'])}</text>
'''

def finish(w=1180,h=470):
    return f'''<path d="M50 {h-63}H1130" stroke="#42636b" stroke-width="1"/><circle cx="58" cy="{h-31}" r="4" fill="#55d8bb"/><text x="75" y="{h-26}" font-family="NanumGothic, Noto Sans CJK KR, Malgun Gothic, Arial, sans-serif" font-size="12" fill="#acc8c5">편집자가 논문을 바탕으로 재구성한 개념도 · 원논문에 수록된 그림이 아닙니다.</text></svg>'''

def flow(pid,fig):
    s=svg_start(pid,fig)
    for i,node in enumerate(fig['nodes']):
        x=42+229*i
        s+=f'<rect x="{x}" y="178" width="205" height="206" rx="17" fill="url(#panel)" stroke="#41646b" stroke-width="1.2"/>'
        s+=f'<rect x="{x}" y="178" width="205" height="4" rx="2" fill="{["#6ed7ca","#e7bc82","#6ec9df","#c4b4ee","#83d5a4"][i]}"/>'
        s+=f'<rect x="{x+18}" y="197" width="44" height="34" rx="8" fill="#2d5d62"/>'
        s+=f'<text x="{x+40}" y="220" text-anchor="middle" font-family="Arial" font-size="15" font-weight="800" fill="#98f3dc">0{i+1}</text>'
        for j,v in enumerate(node[:3]):
            if j==0:
                s+=f'<text x="{x+17}" y="264" font-family="NanumGothic, Noto Sans CJK KR, Malgun Gothic, Arial, sans-serif" font-size="16" font-weight="800" fill="#eafdff">{t(v)}</text>'
            else:
                s+=f'<text x="{x+17}" y="{304+(j-1)*27}" font-family="NanumGothic, Noto Sans CJK KR, Malgun Gothic, Arial, sans-serif" font-size="13" fill="#afcbd0">{t(v)}</text>'
        if i!=4:
            s+=f'<line x1="{x+208}" y1="280" x2="{x+227}" y2="280" stroke="#74d5ca" stroke-width="3" marker-end="url(#arrow)"/>'
    return s+finish()

def cards(pid,fig):
    s=svg_start(pid,fig)
    for i,node in enumerate(fig['nodes']):
        x=42+283*i
        accent=['#5edcca','#f3be91','#9eb9f9','#b7dfa3'][i]
        s+=f'<rect x="{x}" y="172" width="264" height="210" rx="17" fill="#1f3c48" stroke="#40626d" stroke-width="1.2"/>'
        s+=f'<circle cx="{x+35}" cy="205" r="16" fill="{accent}" fill-opacity=".16" stroke="{accent}" stroke-opacity=".65"/>'
        s+=f'<text x="{x+35}" y="211" text-anchor="middle" font-family="Arial" font-size="13" font-weight="700" fill="{accent}">{i+1}</text>'
        s+=f'<text x="{x+19}" y="260" font-family="NanumGothic, Noto Sans CJK KR, Malgun Gothic, Arial, sans-serif" font-size="21" font-weight="800" fill="#f0fffa">{t(node[0])}</text>'
        s+=f'<path d="M{x+18} 283 h224" stroke="#3d6770"/>'
        for j,v in enumerate(node[1:]):
            s+=f'<text x="{x+19}" y="{312+j*31}" font-family="NanumGothic, Noto Sans CJK KR, Malgun Gothic, Arial, sans-serif" font-size="14" fill="#c1dadc">{t(v)}</text>'
    return s+finish()

def bars(pid,fig):
    s=svg_start(pid,fig)
    for i,(label,val) in enumerate(fig['bars']):
        y=171+i*55
        color='#65ddc7' if i==0 else '#8eb0c1'
        bw=round(690*float(val)/100)
        s+=f'<text x="48" y="{y+18}" font-family="NanumGothic, Noto Sans CJK KR, Malgun Gothic, Arial, sans-serif" font-size="16" font-weight="700" fill="#e5f7f8">{t(label)}</text>'
        s+=f'<rect x="392" y="{y}" width="695" height="25" rx="9" fill="#294a53"/>'
        s+=f'<rect x="392" y="{y}" width="{bw}" height="25" rx="9" fill="{color}"/>'
        s+=f'<text x="1090" y="{y+18}" text-anchor="end" font-family="Arial" font-size="16" font-weight="800" fill="#ffffff">{val:.1f}%</text>'
    s+=f'<text x="49" y="{405 if len(fig["bars"])<=4 else 440}" font-family="NanumGothic, Noto Sans CJK KR, Malgun Gothic, Arial, sans-serif" font-size="12" fill="#a9bfc7">막대값은 논문에서 보고한 동일 평가 항목 내 성공률입니다. 서로 다른 평가 환경과 직접 비교하면 안 됩니다.</text>'
    return s+finish(h=500 if len(fig['bars'])>4 else 470)

def render():
    data=json.loads((R/'data/visual_studies.json').read_text(encoding='utf-8'))
    O.mkdir(parents=True,exist_ok=True)
    for pid,study in data.items():
        for fig in study['figures']:
            path=O/f'{pid}-{fig["slug"]}.svg'
            path.write_text({'flow':flow,'cards':cards,'bars':bars}[fig['style']](pid,fig),encoding='utf-8')
            if 'viewBox="0 0 1180 470"' not in path.read_text(): raise ValueError(path)
    print('Built',len(list(O.glob('*.svg'))),'source-safe original figure illustrations')
if __name__=='__main__':render()
