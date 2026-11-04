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
