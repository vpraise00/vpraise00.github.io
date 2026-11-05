"""Offline tests: no personal tokens or network calls."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'scripts'))
from scripts import build_site, update_papers
import deploy

class SiteTests(unittest.TestCase):
    def test_curated_corpus_and_categories(self):
        p=json.loads((ROOT/'data/papers.json').read_text(encoding='utf8'))['papers']
        c=json.loads((ROOT/'config/topics.json').read_text(encoding='utf8'))['categories']
        self.assertGreaterEqual(len(p),15)
        self.assertTrue({'vla','wam','robotics'}.issubset({a['primary_category'] for a in p}))
        ids=[a['id'] for a in p]
        self.assertEqual(len(ids),len(set(ids)))
        for a in p:
            self.assertRegex(a['id'],r'^\d{4}\.\d{4,5}$')
            self.assertTrue(a['source_url'].endswith(a['id']))
            for k in ('problem','idea','method','findings','limitations','questions'):
                self.assertIn(k,a['review'])
        self.assertTrue(all(ca['queries'] for ca in c[:3]))

    def test_curated_deep_dive_is_substantial_and_source_scoped(self):
        papers=json.loads((ROOT/'data/papers.json').read_text(encoding='utf-8'))['papers']
        for paper in papers:
            if not paper.get('curated'):
                continue
            deep=paper.get('deep_dive') or {}
            self.assertGreaterEqual(len(deep.get('pipeline',[])),3,paper['id'])
            self.assertGreaterEqual(len(deep.get('mechanisms',[])),2,paper['id'])
            self.assertGreaterEqual(len(deep.get('evidence',[])),2,paper['id'])
            self.assertGreaterEqual(len(deep.get('reading_guide',[])),3,paper['id'])
            self.assertTrue(deep.get('replication',{}).get('baselines'),paper['id'])
            self.assertGreater(len(json.dumps(deep,ensure_ascii=False)),2200,paper['id'])
            html=build_site.post_page(paper,{'vla':{'label':'VLA','color':'#238f7c'},'wam':{'label':'WAM','color':'#238f7c'},'robotics':{'label':'Robotics','color':'#238f7c'}})
            self.assertGreaterEqual(html.count('class="pipeline-step"'),3,paper['id'])
            self.assertGreaterEqual(html.count('class="mechanism-card"'),2,paper['id'])
            self.assertGreaterEqual(html.count('<tr><td>'),2,paper['id'])
            self.assertIn('후속 실험 제안',html,paper['id'])
            self.assertIn('초록 기반 한국어 요약',html,paper['id'])

    def test_original_figures_are_source_grounded_not_redrawn(self):
        entries=json.loads((ROOT/'data/figure_catalog.json').read_text(encoding='utf8'))
        pages={x['id'] for x in json.loads((ROOT/'data/papers.json').read_text(encoding='utf8'))['papers']}
        self.assertEqual(set(entries),pages)
        self.assertEqual(sum(len(item['figures']) for item in entries.values()),32)
        for pid,item in entries.items():
            html=(ROOT/'papers'/f'{pid}.html').read_text(encoding='utf8')
            self.assertNotIn('id="visual-lab"',html)
            self.assertIn('class="original-paper-figure inline-source-figure"',html)
            self.assertTrue('원본 이미지 확인 대기' in html or 'arXiv HTML 저자 원본' in html or '원논문 PDF 자동 추출' in html)
            self.assertEqual(html.count('class="original-paper-figure inline-source-figure"'),2,pid)
            self.assertNotIn('class="research-figure editorial-figure"',html,pid)
            self.assertNotIn(f'../assets/figures/{pid}-',html,pid)
            self.assertIn('원문을 읽으면서 확인할 4가지',html,pid)


    def test_source_figures_follow_their_method_or_result_explanations(self):
        papers=json.loads((ROOT/'data/papers.json').read_text(encoding='utf8'))['papers']
        cats={c:{'label':c.upper(),'color':'#2a8a82'} for c in ('vla','wam','robotics')}
        for p in papers:
            html=build_site.post_page(p,cats)
            fig_positions=[]
            # Ensure no source figure is placed before the problem statement.
            first=html.find('class="original-paper-figure inline-source-figure"')
            self.assertGreater(first,html.index('id="problem"'),p['id'])
            for n, placement in build_site.FIGURE_PLACEMENTS.get(p['id'],{}).items():
                pos=html.index('id="original-figure-'+str(n)+'"')
                self.assertGreater(pos,html.index('id="'+ ('idea' if placement=='comparison' else placement) +'"'),(p['id'],n))
                if placement=='method':
                    self.assertLess(pos,html.index('id="findings"'),(p['id'],n))
                if placement=='findings':
                    self.assertLess(pos,html.index('id="limitations"'),(p['id'],n))
                fig_positions.append(pos)
            self.assertEqual(len(fig_positions),2,p['id'])
            self.assertIn('id="pipeline"',html,p['id'])

    def test_ten_am_cron_and_edit_trigger(self):
        workflow=(ROOT/'.github/workflows/daily-research.yml').read_text(encoding='utf8')
        self.assertIn("cron: '0 1 * * *'",workflow)
        self.assertIn("'scripts/build_site.py'",workflow)
        self.assertIn('workflow_dispatch:',workflow)
        self.assertIn('git pull --rebase origin main',workflow)

    def test_source_figure_detection_and_pdf_crop(self):
        import fitz
        from scripts import extract_paper_figures as ex
        self.assertEqual(ex.caption_number('Figure 2: Architecture overview'),2)
        self.assertEqual(ex.caption_number('Fig. 12. Experiments'),12)
        self.assertIsNone(ex.caption_number('Our method is described in Figure 2:'))
        doc=fitz.open(); pg=doc.new_page(width=595,height=842)
        pg.draw_rect(fitz.Rect(60,180,530,350),color=(0.1,0.4,0.6),fill=(0.2,0.8,0.3))
        pg.insert_text((70,375),'Figure 2: A genuine figure from this synthetic PDF document.',fontsize=10)
        matching=ex.pdf_captions(doc)
        self.assertIn(2,matching)
        png,size,rect=ex.crop_from_pdf(doc,matching[2])
        self.assertTrue(png.startswith(b'\x89PNG'))
        self.assertGreater(size[0],400)
        self.assertGreater(len(png),1500)
        self.assertLess(rect[1],340)

    def test_arxiv_atom_parsing(self):
        feed=b'''<feed xmlns="http://www.w3.org/2005/Atom"><entry>
        <id>http://arxiv.org/abs/2610.42021v2</id><title> New   VLA \nPaper </title>
        <summary>A robot action and world-action paper with useful manipulation experiments.</summary>
        <published>2026-10-30T03:00:00Z</published><updated>2026-10-31T00:00:00Z</updated>
        <author><name>Alice</name></author><category term="cs.RO"/></entry></feed>'''
        papers=update_papers.parse_feed(feed)
        self.assertEqual(papers[0]['id'],'2610.42021')
        self.assertEqual(papers[0]['title'],'New VLA Paper')
        self.assertEqual(papers[0]['authors'],['Alice'])
        self.assertEqual(papers[0]['published'],'2026-10-30')
        self.assertIn('cs.RO',papers[0]['arxiv_categories'])

    def test_canonical_slug_and_xss(self):
        with self.assertRaises(ValueError): build_site.clean_slug('../evil')
        paper=json.loads((ROOT/'data/papers.json').read_text(encoding='utf-8'))['papers'][0].copy()
        paper['title']='Hello </script><script>alert(1)</script>'
        html=build_site.post_page(paper,{'vla':{'label':'VLA','color':'#2a8a82'}})
        self.assertNotIn('<script>alert(1)</script>',html)
        self.assertIn('&lt;script&gt;',html)
        self.assertIn('\\u003c',html)

    def test_build_outputs(self):
        build_site.build()
        self.assertTrue((ROOT/'papers/2610.07922.html').exists())
        self.assertIn('GPT', (ROOT/'papers/2610.07922.html').read_text(encoding='utf8'))
        self.assertIn('2609.16074', (ROOT/'sitemap.xml').read_text())
        self.assertIn('Research Radar', (ROOT/'feed.xml').read_text())

    def test_local_env_only_and_safe_file_collector(self):
        with tempfile.TemporaryDirectory() as tmp:
            f=Path(tmp)/'.env'
            f.write_text('GITHUB_TOKEN="exampletoken"\nOPENAI_API_KEY=do-not-log-me\n',encoding='utf8')
            parsed=deploy.dotenv(f)
            self.assertEqual(parsed['GITHUB_TOKEN'],'exampletoken')
        names=dict(deploy.collect_files())
        self.assertIn('.github/workflows/daily-research.yml',names)
        self.assertNotIn('.env',names)
        self.assertTrue(all(not s.startswith('.env') for s in names))

if __name__=='__main__':unittest.main()
