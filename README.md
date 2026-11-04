# Embodied Research Radar

**VLA · World-Action Models · Robotics** 연구 논문을 한국어로 탐색하고, 논문별 상세 해설을 읽고, 중요한 문장에 표시하며 ChatGPT에 질문하는 GitHub Pages 연구 노트입니다.

- 사이트(배포 후): **https://vpraise00.github.io/**
- GitHub 저장소(배포 후): **https://github.com/vpraise00/vpraise00.github.io**

## 1. 가장 간단한 설치 방법 (Windows)

1. ZIP 파일을 원하는 폴더에 **전체 압축 해제**합니다. `deploy.py`, `index.html`, `assets/`, `config/`, `.github/`가 같은 폴더 구조에 있어야 합니다.
2. 기존 `D:\vpraise\.env`에 `GITHUB_TOKEN=...` (혹은 `GH_TOKEN`, `GITHUB_PAT`)이 있는지 **자신의 PC에서만** 확인합니다. 토큰을 웹페이지, 채팅, 커밋에 붙여넣지 마세요.
3. PowerShell에서 압축 해제한 폴더로 이동해 다음 명령을 실행합니다.

```powershell
py deploy.py --env "D:\vpraise\.env" --owner vpraise00
```

- 스크립트는 **연동 계정 이름 확인 → 공개 `vpraise00.github.io` 저장소 생성 → 파일 업로드 → Pages 브랜치 배포 활성화**를 수행합니다.
- 토큰은 **파일에 기록하거나 출력하지 않습니다**. `.env` 파일도 업로드에서 자동 제외됩니다.
- GitHub 토큰에는 새 공개 저장소 생성·콘텐츠 변경·워크플로 업로드·Pages 설정 권한이 필요합니다. Fine-grained PAT는 저장소 생성/관리 및 Actions 워크플로 관련 권한을 확인하세요.
- 기존 저장소가 있으면 그 저장소에 동명의 사이트 파일을 업데이트합니다. 사용 중인 GitHub Pages 저장소라면 먼저 백업하세요.
- 아래의 `--dry-run`은 외부 접속 없이 업로드될 파일만 확인합니다.

```powershell
py deploy.py --dry-run
```

페이지가 표시되지 않으면 <https://github.com/vpraise00/vpraise00.github.io/settings/pages>에서 **Deploy from a branch → main → /(root)** 를 선택합니다. GitHub Pages는 별도의 항상 켜진 서버가 아니라 정적 웹 호스팅입니다.

## 논문 상세 분석 — Researcher Edition

- 시작할 때 제공되는 **큐레이션 16편 모두** 한국어 기술 해설을 포함합니다. 단순 5문단 요약을 넘어 **작동 순서 3–5단계, 알고리즘·학습 신호, 근거/성능표, 기존 방법과 비교, 원문 정독 체크리스트, 재현 실험 설계와 변인 통제, 관련 논문 연결**을 제공합니다.
- 논문 저자가 실제로 보고한 숫자와 **편집자가 제안한 후속 실험**을 별도 섹션으로 분리했습니다. arXiv 초록/공식 프로젝트 자료에서 확인할 수 없는 실험 수치는 창작하지 않습니다. 초록 영역의 큐레이션 한국어 글은 **공식 영문 Abstract의 번역이 아닌 편집자 요약**이라는 설명을 표시합니다.
- 수기 보강 콘텐츠는 `scripts/deep_content.py`에서 수정 후 `python scripts/enrich_curated.py && python scripts/build_site.py`로 전체 페이지를 갱신할 수 있습니다. 기본 데이터는 `data/papers.json`에 저장됩니다.
- 향후 arXiv 자동 수집 포스팅도 `OPENAI_API_KEY`가 설정되어 있고 AI 분석에 성공하면 구조화된 **Deep Dive**(모델 처리 흐름·근거표·재현안)를 생성합니다. **키가 없거나 API/PDF 분석에 실패하면 초록 기반 미리보기만** 생성합니다. 전체 PDF 검증이 불가능한 경우 출처 범위를 명시합니다. 잘못된 숫자·근거 없는 모듈 설명을 채워 넣는 대신 미확인이라고 표기합니다.


## 원논문 Figure 원본 기반 상세 해설 (전체 16편)

**이전 편집 제작 SVG 15개는 제거했습니다. 원논문의 그림인 것처럼 표시하지 않습니다.**

- `data/figure_catalog.json`에는 초기 16편 각각의 Figure 번호, 해당 논문을 이해하기 위해 확인할 맥락, 각 그림의 독해 포인트를 편집자가 기록했습니다. **32개 Figure 후보**입니다.
- `scripts/extract_paper_figures.py`는 arXiv 논문 HTML에서 **Figure 번호와 캡션이 일치하는 원저자 이미지만** 복사합니다. HTML에서 얻을 수 없을 때에는 원문 PDF에서 **해당 Figure 캡션을 실제로 검출한 페이지 영역**을 PNG로 렌더링합니다. 이 PDF 크롭은 *자동 추출, 검수 필요* 상태입니다.
- 원본 이미지는 `assets/paper-figures/`에 보관되고, 추출 이력은 `data/figure_extract_status.json`에 파일·출처·원본 캡션 일부·PDF 페이지·추출 방법과 검수 상태로 기록됩니다.
- 매일 실행되는 `Source figure refresh` 워크플로가 원문 이미지를 갱신합니다. 추출 실패 시에는 그림을 임의로 만들지 않고 원문 PDF 링크만 보여줍니다. GitHub Actions·네트워크 사정에 따라 일부 이미지가 확보되지 않을 수 있습니다.
- 그림 아래 한국어 문장은 편집자의 **해석·연구 맥락 가이드**이며 원저자의 Figure 캡션을 번역했다고 주장하지 않습니다. 직접 인용된 캡션은 최대 22단어만 표시하고 원문을 링크합니다.
- 실제로 그림의 내용이 잘려 있거나 그림 번호가 틀렸다면 `data/figure_extract_status.json`의 `review`와 크롭 영역을 확인해야 합니다. 공개 게시 전에 사람이 직접 시각 검수하는 것을 권장합니다.
- 기존 설명 본문의 문제 정의·방법론·실험 결과·한계·연구 재현 가이드와 GPT 질문, 북마크 및 메모는 그대로 사용할 수 있습니다.

원본 그림 수집 수동 명령:

```bash
python -m pip install -r requirements.txt
python scripts/extract_paper_figures.py
python scripts/build_site.py
```

**저작권:** 논문 그림은 원저자에게 권리가 있습니다. 논문의 라이선스/저자 허락을 확인하고, 짧은 그림 인용만 출처를 표기한 해설 목적으로 사용하세요. 무제한 재배포할 수 있다는 의미는 아닙니다.

## 2. 매일 새로운 논문 자동 갱신

`.github/workflows/daily-research.yml`이 **매일 UTC 00:15 / 한국시간 09:15경** 실행되어 arXiv에서 세 카테고리를 검색하고, 중복 제거·논문별 HTML·RSS·sitemap을 생성한 뒤 자동으로 커밋합니다. GitHub Actions의 스케줄은 지연될 수 있습니다.

- 새 논문은 기존 큐레이션 글과 구분되어 `자동 수집 · 초록 기반 요약`으로 표시됩니다.
- 논문 PDF를 읽어 **한국어 심층 요약**을 자동 작성하려면 `OPENAI_API_KEY`를 GitHub 저장소 **Settings → Secrets and variables → Actions → New repository secret**에 등록합니다. PDF 텍스트 추출은 가능한 경우에만 수행되며, AI 글에는 정확성 재확인 안내를 표시합니다.
- 로컬 `.env`에 `OPENAI_API_KEY`가 있고 `py -m pip install pynacl`이 설치된 경우, `deploy.py`가 GitHub 공개키로 암호화해 해당 secret 등록을 시도할 수 있습니다.
- API 사용에는 OpenAI API 과금이 발생할 수 있습니다. 새 글 수 제한은 `config/topics.json`의 `max_new_per_run`을 수정하세요. 모델은 GitHub Actions 변수 `OPENAI_MODEL`로 설정 가능합니다 (기본 `gpt-4.1-mini`).
- 수동 실행: 저장소 **Actions → Daily research radar → Run workflow**.
- API 장애 시 작업은 실패 상태를 남기고 이전 데이터를 보존합니다. 수집이 성공했다면 `last_checked`를 새로 기록합니다.

## 3. 카테고리 맞춤 설정

- **브라우저 개인용:** 사이트에서 `분류 직접 설정하기`를 눌러 카테고리 추가·이름/키워드 변경·순서 이동·삭제할 수 있습니다. 브라우저의 `localStorage`에 저장되므로 개인별로 분류가 다를 수 있습니다.
- **전체 사이트 및 자동 수집:** GitHub의 [`config/topics.json`](https://github.com/vpraise00/vpraise00.github.io/edit/main/config/topics.json)을 수정합니다. `id`, `label`, `description`, `color`(`#RRGGBB`), `keywords`, arXiv의 `queries`를 관리할 수 있습니다. 다음 스케줄 실행부터 신규 수집에 반영됩니다. 분류 규칙을 바꾸면 기존 논문 분류를 일괄 변경하진 않습니다.
- 개인 노트/북마크/하이라이트/분류 설정은 설정 패널에서 JSON으로 **내보내기/가져오기** 가능합니다. 사이트 방문자 사이에 자동 동기화되지는 않습니다.

## 4. 논문 읽기 기능

- 논문마다 `papers/<arxiv-id>.html` 별도 URL, 한국어 구조화 해설, 인용 출처와 PDF 링크.
- 논문 본문에서 텍스트 드래그 → **하이라이트 저장**, **선택 부분 GPT에 질문**.
- ChatGPT 질문 버튼은 `chatgpt.com/?q=` 형식의 링크로 논문 제목·원문 링크·선택 문장을 전달합니다. **ChatGPT 계정 로그인이 필요할 수 있습니다.** 링크 서비스 방식에 따라 자동 입력/전송 동작이 달라질 수 있으므로 `질문 내용 복사하기`도 제공합니다. OpenAI API key가 사이트에 공개되거나 브라우저에서 호출되지는 않습니다.
- 메모와 북마크는 브라우저 저장소에 머무르며, 기기를 바꾸거나 브라우저 데이터를 삭제하면 없어질 수 있습니다. 개인 데이터는 정기적으로 JSON으로 백업하세요.

## 5. 로컬 미리보기와 구조

```bash
python scripts/build_site.py
python -m http.server 8000
# http://localhost:8000
```

```
assets/                  styles.css, shared.js, home.js, paper.js
config/topics.json       카테고리·키워드·arXiv 검색식
data/papers.json         논문 데이터 + 편집/자동 해설
papers/*.html            논문별 독립적인 정적 URL
scripts/seed_content.py  최초 16편 데이터 생성 스크립트(기존 데이터 덮어씀)
scripts/update_papers.py 매일 arXiv 수집 / AI 선택적 분석
scripts/build_site.py    정적 HTML·RSS·sitemap 생성
.github/workflows/       일간 업데이트 GitHub Actions
index.html               메인 페이지
deploy.py                 로컬 토큰을 쓰는 최초 배포 프로그램
```

`seed_content.py`는 재초기화용이므로 **일반적인 업데이트에는 실행하지 마세요.** 심층 해설을 수동 수정하려면 `data/papers.json`의 `review`를 편집하고 `python scripts/build_site.py`를 실행합니다. 수동 큐레이션 논문은 자동 업데이트 과정에서 덮어쓰지 않습니다.

## 연구 정보와 주의점

- 초기 큐레이션 글은 2026-11-04 기준, 원문 arXiv 링크와 관련 공식 프로젝트 정보를 확인하고 작성했습니다. 'Hot'은 편집자의 관심 논문 선정이지 자동 인용수/평점 순위가 아닙니다.
- 자동 생성된 글은 정보 출처 범위(`abstract` 또는 `pdf+abstract`)를 표시합니다. AI 작성 결과는 틀릴 수 있으므로 원문으로 검증하세요.
- 이 저장소는 **정적 사이트**이며 서버에서 방문자 질문을 중계하거나 개인 노트를 저장하지 않습니다. 별도의 서버나 로그인 연동을 하지 않는 한 개인 노트의 기기간 자동 동기화는 지원하지 않습니다.

© Research Radar. Paper titles and source links credited to their authors.
