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

    def test_visual_paper_walkthrough_has_attribution_and_images(self):
        ids=['2610.07922','2608.01397','2504.16054','2610.42021','2610.40026']
        visual=json.loads((ROOT/'data/visual_studies.json').read_text(encoding='utf8'))
        for pid in ids:
            self.assertIn(pid,visual)
            story=visual[pid]
            self.assertEqual(len(story['figures']),3)
            html=(ROOT/'papers'/f'{pid}.html').read_text(encoding='utf8')
            self.assertIn('그림으로 논문 하나씩 뜯어보기',html)
            self.assertIn('원본 Figure가 아닙니다',html)
            self.assertEqual(html.count('class="research-figure editorial-figure"'),3)
            self.assertIn('실제로 구현하고 검증한다면',html)
            self.assertGreaterEqual(html.count('class="figure-detail"'),10)
            for fig in story['figures']:
                path=ROOT/'assets'/'figures'/f"{pid}-{fig['slug']}.svg"
                self.assertTrue(path.exists(),str(path))
                svg=path.read_text(encoding='utf8')
                self.assertIn('viewBox="0 0 1180 470"',svg)
                self.assertIn('편집자가 논문을 바탕으로 재구성한 개념도',svg)
                self.assertNotIn('<script',svg)
        self.assertIn('원저자 원본 출처',(ROOT/'papers/2608.01397.html').read_text(encoding='utf8'))

    def test_visual_diagrams_are_well_formed_svg(self):
        import xml.etree.ElementTree as ET
        files=list((ROOT/'assets'/'figures').glob('*.svg'))
        self.assertGreaterEqual(len(files),15)
        for path in files:
            root=ET.parse(path).getroot()
            self.assertTrue(root.tag.endswith('svg'),path.name)

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
