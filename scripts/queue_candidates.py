#!/usr/bin/env python3
"""Daily discovery without public posting. Leaves published data and HTML unchanged."""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts import update_papers as arxiv
ROOT=Path(__file__).resolve().parents[1]
QUEUE=ROOT/'data/review_queue.json'

def discover(config, fetcher=arxiv.fetch_atom):
    old=json.loads(QUEUE.read_text(encoding='utf-8')) if QUEUE.exists() else {'candidates':[]}
    approvals=json.loads((ROOT/'data/editorial_approvals.json').read_text(encoding='utf-8'))
    existing=json.loads((ROOT/'data/papers.json').read_text(encoding='utf-8'))
    approved=set(approvals.get('approved_ids',[]))
    rows={r['id']:r for r in old.get('candidates',[]) if r.get('id') and r['id'] not in approved}
    # Archive all previously autoposted/uncrosschecked articles as review candidates.
    for p in existing.get('papers',[]):
        if p.get('id') in approved: continue
        rows.setdefault(p['id'],{'id':p['id'],'title':p['title'],'authors':p.get('authors',[]),'published':p.get('published',''),'source_url':f'https://arxiv.org/abs/{p["id"]}','status':'awaiting_full_text_review','source':'previously_published_draft'})
    errors=[];seen=set();discovered=0
    for category in config.get('categories',[]):
        for q in category.get('queries',[])[:2]:
            if q in seen:continue
            seen.add(q)
            try:feed=arxiv.parse_feed(fetcher(q, min(16,int(config.get('update',{}).get('max_results_per_query',16)))))
            except Exception as ex:
                errors.append(type(ex).__name__+': '+q);continue
            for p in feed:
                if p['id'] in rows or p['id'] in approved:continue
                # Discovery relevance is intentionally broad; publication requires independent source verification.
                if not arxiv.is_relevant(p):continue
                rows[p['id']]={'id':p['id'],'title':p['title'],'authors':p.get('authors',[])[:8],
                   'published':p['published'],'source_url':p['source_url'],'status':'awaiting_full_text_review','source':'arxiv_metadata_only'}
                discovered+=1
    if errors and discovered==0 and not old.get('candidates'):
        raise RuntimeError('All arXiv discovery queries failed; refusing to call a stale queue updated. '+str(errors[:2]))
    queue={'last_checked':datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z'),'publication_mode':'manual_approval_only','discovered_this_run':discovered,
      'errors':errors,'candidates':sorted(rows.values(),key=lambda p:(p.get('published',''),p['id']),reverse=True)[:200]}
    QUEUE.write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'candidate queue: {len(queue["candidates"])} papers. no posts are published.')
    return queue

if __name__=='__main__':
 config=json.loads((ROOT/'config/topics.json').read_text(encoding='utf-8'))
 discover(config)
