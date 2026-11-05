# Research Radar — editorial policy (2026-11-05)

The site is a **source-verified research reading notebook**, not an auto-publishing arXiv mirror.

## Rules

1. **Every day at ~10:00 KST**, `daily-research.yml` searches arXiv metadata and writes only `data/review_queue.json`. No article, RSS, sitemap, or `data/papers.json` is generated in the scheduled workflow.
2. Drafts (including older automatically published digests) are **not public**. Source data is preserved in git history and `data/papers.json`; the browser and site generator render only IDs present in `data/editorial_approvals.json` with an audited record in `data/editorial_content.json`.
3. An article may be approved only after confirming the correct paper/title/ID, reading the paper's **Method, Experiments and relevant Appendix**, matching figure number and caption to an author-provided image, distinguishing observations from conclusions, and adding ablation/baselines/failure conditions.
4. A figure appears **where the specific method or experiment is explained**, not as a cover gallery. Crop-derived figures require extra manual review; invented or stock figures are not substitutes.
5. All paper results are author claims. We do not claim independent experimental reproducibility. Original figures are attributed and linked.
6. Missing evidence means **withhold publication**, not filler prose. New approved articles must be individually added to both `data/editorial_content.json` and `data/editorial_approvals.json`, then rebuilt with `python scripts/build_site.py`.
7. `source-figures.yml` runs manually only. Daily candidate discovery must not alter published figure content.

## Why the public list got smaller

On Nov 5, 2026, automatically generated posts were determined to be too shallow. We have kept their information in a private-by-policy editorial backlog (repository data) but removed them from the public index, RSS, sitemap, and HTML output. Only source-crosschecked articles are visible. Existing users' browser localStorage notes/bookmarks are not erased.
