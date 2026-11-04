#!/usr/bin/env python3
"""Fetch *actual author figures*, never synthesize substitute images.

First attempt to copy the figure image from arXiv's converted paper HTML using
an explicitly matched caption number. When not available, render a localized
crop of the corresponding figure from the original arXiv PDF. The extraction
status records source, page, and provenance; failed figures stay unfilled.

Automatic crops are marked 'needs_manual_review'; never label them verified.
"""
from __future__ import annotations
import argparse
import io
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'assets'/'paper-figures'
CATALOG=ROOT/'data'/'figure_catalog.json'
STATUS=ROOT/'data'/'figure_extract_status.json'
UA={'User-Agent':'EmbodiedResearchRadar/1.0 (scholarly figure attribution; https://github.com/vpraise00/vpraise00.github.io)'}
FIG_RE=re.compile(r'^\s*(?:Figure|Fig\.?)[\s\u00a0]*([0-9]{1,2})\s*(?::|\.|\s)',re.I)


def caption_number(text):
    m=FIG_RE.match(text.strip())
    return int(m.group(1)) if m else None


def network_get(session,url,max_bytes=45_000_000):
    """Don't let an unexpectedly large manuscript crash the workflow."""
    import requests
    for i in range(3):
        try:
            r=session.get(url,headers=UA,timeout=(16,55),stream=True,allow_redirects=True)
            if r.status_code in (429,502,503,504):
                r.close(); time.sleep(2+i*5); continue
            r.raise_for_status()
            data=bytearray()
            for block in r.iter_content(1<<17):
                data.extend(block)
                if len(data)>max_bytes:raise ValueError(f'File too big ({len(data)})')
            r.close()
            return bytes(data)
        except (requests.RequestException,ValueError) as e:
            if i==2:raise
            time.sleep(2+i*4)
    raise RuntimeError(url)


def parse_html_figures(session, paper_id):
    from bs4 import BeautifulSoup
    for v in ('', 'v1'):
        page=f'https://arxiv.org/html/{paper_id}{v}'
        try:
            html=network_get(session,page,max_bytes=4_000_000).decode('utf-8',errors='replace')
            soup=BeautifulSoup(html,'html.parser')
            entries={}
            for fig in soup.select('figure'):
                cap=fig.select_one('figcaption')
                if not cap:continue
                caption=' '.join(cap.stripped_strings)
                n=caption_number(caption)
                if n is None or n in entries:continue
                img=fig.select_one('img[src]')
                if not img:continue
                src=img.get('src','')
                if src.startswith('data:') or src.startswith('javascript:'):continue
                # arXiv HTML uses paper-relative assets. urljoin('/html/IDv1',
                # 'x2.png') is WRONG and drops the ID. Anchor under /html/IDv1/.
                if src.startswith(('http://','https://')):
                    image_url=src
                elif src.startswith('/'):
                    image_url=urljoin('https://arxiv.org',src)
                elif re.match(r'^\d{4}\.\d{4,5}v\d+/',src):
                    image_url='https://arxiv.org/html/'+src
                else:
                    image_url=page.rstrip('/')+'/'+src.lstrip('./')
                entries[n]={'url':image_url,'caption':caption[:850],'article':page,'anchor':fig.get('id','')}
            if entries:return entries
        except Exception as exc:
            print(f'[HTML] {paper_id}: {str(exc)[:140]}',flush=True)
    return {}


def image_to_png(data):
    from PIL import Image
    im=Image.open(io.BytesIO(data))
    im.load()
    if im.width<220 or im.height<65:
        raise ValueError(f'figure image too small: {im.size}')
    if im.width>4500 or im.height>8000:
        im.thumbnail((4500,8000))
    if im.mode not in ('RGB','RGBA'):im=im.convert('RGB')
    output=io.BytesIO(); im.save(output,format='PNG',optimize=True)
    return output.getvalue(),(im.width,im.height)


def source_html_image(session,entry):
    import fitz
    url=entry['url']
    raw=network_get(session,url,max_bytes=18_000_000)
    if raw[:4]==b'%PDF':
        doc=fitz.open(stream=raw,filetype='pdf')
        pix=doc[0].get_pixmap(matrix=fitz.Matrix(1.7,1.7),alpha=False)
        return pix.tobytes('png'),(pix.width,pix.height)
    if raw.lstrip().startswith(b'<svg'):
        try:
            import cairosvg
            return image_to_png(cairosvg.svg2png(bytestring=raw))
        except ImportError:raise RuntimeError('SVG image needs cairosvg')
    return image_to_png(raw)


def pdf_captions(doc):
    """Only match text lines that START with Figure N, not citations in prose."""
    matches={}
    for page_idx,page in enumerate(doc):
        d=page.get_text('dict')
        for block in d.get('blocks',[]):
            if block.get('type')!=0:continue
            lines=block.get('lines',[])
            for i,line in enumerate(lines):
                txt=''.join(span['text'] for span in line.get('spans',[])).strip()
                num=caption_number(txt)
                if num is None or num in matches:continue
                rest=[]
                for sub in lines[i:i+5]:
                    s=''.join(span['text'] for span in sub.get('spans',[])).strip()
                    if s:rest.append(s)
                    if sum(len(q) for q in rest)>380:break
                caption=' '.join(rest).strip()[:650]
                if len(caption)<15:continue
                matches[num]={'page':page_idx,'bbox':tuple(line['bbox']),'caption':caption}
    return matches


def crop_from_pdf(doc,rec):
    import fitz
    page=doc[rec['page']]
    rect=page.rect
    x0,y0,x1,y1=rec['bbox']
    middle=rect.width/2
    # Determine the figure band from the caption's column. Wide figures cross columns.
    if x0<middle-30 and x1<middle+12:
        left,right=30,middle-6
    elif x0>middle-14:
        left,right=middle+4,rect.width-28
    else:
        left,right=25,rect.width-25
    # Figure usually sits immediately above its caption. Keep its *original*
    # page content intact, including vector drawing and labels.
    band_height=270 if right-left<rect.width*.65 else 348
    top=max(24,y0-band_height)
    bottom=min(rect.height-24,y1+35)
    if bottom-top<100:raise ValueError('caption near page edge; cannot safely crop')
    clip=fitz.Rect(left,top,right,bottom)
    pix=page.get_pixmap(matrix=fitz.Matrix(1.8,1.8),clip=clip,alpha=False)
    return pix.tobytes('png'),(pix.width,pix.height),tuple(round(v,1) for v in clip)


def pdf_fallback(session,id,wanted):
    import fitz
    raw=None
    for url in [f'https://arxiv.org/pdf/{id}',f'https://export.arxiv.org/pdf/{id}',f'https://arxiv.org/pdf/{id}.pdf']:
        try:
            candidate=network_get(session,url,max_bytes=48_000_000)
            if candidate.startswith(b'%PDF'):
                raw=candidate;break
        except Exception as e:
            print(f'[PDF] {id}: {str(e)[:130]}',flush=True)
    if not raw:return {}
    doc=fitz.open(stream=raw,filetype='pdf')
    matches=pdf_captions(doc)
    results={}
    for n in wanted:
        rec=matches.get(n)
        if not rec:continue
        try:
            data,size,clip=crop_from_pdf(doc,rec)
            results[n]={'png':data,'size':size,'caption':rec['caption'],'page':rec['page']+1,'clip':clip,'method':'pdf_page_crop','review':'needs_manual_review'}
        except Exception as e:print(f'[PDF CROP] {id} Figure {n}: {e}',flush=True)
    return results


def extract(max_papers=100,refresh=False):
    import requests
    catalog=json.loads(CATALOG.read_text(encoding='utf-8'))
    prev=json.loads(STATUS.read_text(encoding='utf-8')) if STATUS.exists() else {}
    OUTPUT.mkdir(parents=True,exist_ok=True)
    out={}
    session=requests.Session()
    for index,(pid,entry) in enumerate(catalog.items()):
        if index>=max_papers:break
        if not re.fullmatch(r'\d{4}\.\d{4,5}',pid):raise ValueError(pid)
        print(f'[{index+1}/{min(len(catalog),max_papers)}] {pid}',flush=True)
        result={}
        wanted={int(f['number']) for f in entry['figures']}
        missing=set(wanted)
        for n in list(missing):
            path=OUTPUT/f'{pid}-fig{n}.png'
            prevrec=(prev.get(pid) or {}).get(str(n))
            if path.exists() and path.stat().st_size>5_000 and prevrec and not refresh:
                result[str(n)]=prevrec;missing.remove(n)
        if missing:
            html_figs=parse_html_figures(session,pid)
            for n in list(missing):
                rec=html_figs.get(n)
                if not rec:continue
                try:
                    png,size=source_html_image(session,rec)
                    local=OUTPUT/f'{pid}-fig{n}.png';local.write_bytes(png)
                    result[str(n)]={'local':f'assets/paper-figures/{local.name}','source':rec['url'],'paper_source':rec['article'],
                      'caption':rec['caption'],'method':'arxiv_html_exact_figure','review':'caption_matched','dimensions':size}
                    missing.remove(n)
                    print(f' ✓ Figure {n} original HTML illustration {size}',flush=True)
                except Exception as exc:
                    print(f' - HTML image fail Figure {n}: {str(exc)[:125]}',flush=True)
        if missing:
            extracted=pdf_fallback(session,pid,missing)
            for n,rec in extracted.items():
                local=OUTPUT/f'{pid}-fig{n}.png';local.write_bytes(rec['png'])
                result[str(n)]={'local':f'assets/paper-figures/{local.name}','source':f'https://arxiv.org/pdf/{pid}',
                  'paper_source':f'https://arxiv.org/abs/{pid}', 'caption':rec['caption'],
                  'method':rec['method'],'page':rec['page'],'clip':rec['clip'],'review':rec['review'], 'dimensions':rec['size']}
                missing.remove(n)
                print(f' ✓ Figure {n} original PDF crop, page {rec["page"]} (automatic review)',flush=True)
        if missing:print(f' ! {pid}: unavailable original figures {sorted(missing)}; no substitutes generated',flush=True)
        out[pid]=result
        time.sleep(.8)
    STATUS.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Completed: {sum(len(r) for r in out.values())} / {sum(len(e["figures"]) for e in catalog.values())} figures available')
    return out

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--limit',type=int,default=100)
    parser.add_argument('--refresh',action='store_true')
    opts=parser.parse_args()
    extract(opts.limit,opts.refresh)
