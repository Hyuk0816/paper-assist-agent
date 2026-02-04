# PaperAssist

**학술 논문 분석을 위한 Claude Code 에이전트 도구**

PDF 논문에서 수식을 추출하고, 섹션별로 상세 분석하며, 인용 가치를 판단하고, 연구 로그를 자동으로 생성합니다.

---

## 목차

- [주요 기능](#주요-기능)
- [설치](#설치)
- [프로젝트 초기화](#프로젝트-초기화)
- [사용법](#사용법)
- [파일 명명 규칙](#파일-명명-규칙)
- [분석 로그 구조](#분석-로그-구조)
- [인용 가치 판단](#인용-가치-판단)
- [하이브리드 저장소](#하이브리드-저장소)
- [MCP 서버 연동](#mcp-서버-연동)
- [CLI 명령어](#cli-명령어)
- [의존성](#의존성)
- [문제 해결](#문제-해결)

---

## 주요 기능

| 기능 | 설명 |
|------|------|
| **PDF 수식 추출** | pix2tex를 사용하여 LaTeX 형식으로 수식 자동 추출 |
| **섹션별 상세 분석** | 논문 구조를 파악하고 중요 섹션(Methodology, Experiments 등)을 상세 분석 |
| **인용 가치 판단** | Must / Optional / Avoid 등급으로 자동 분류 |
| **연구 로그 자동 생성** | 분석 결과를 체계적인 마크다운으로 저장 |
| **하이브리드 저장소** | GitHub(텍스트/로그) + Google Drive(PDF) 동기화 |
| **날짜별 기록** | `YYYYMMDD_Author_Title` 형식으로 체계적 관리 |

---

## 설치

### 요구사항

- **Python**: 3.10 이상
- **Claude Code CLI**: 설치 및 로그인 완료
- **Git**: 버전 관리용

### 권장: pipx로 설치 (macOS/Linux)

`pipx`는 Python CLI 도구를 격리된 환경에서 실행하므로 시스템 Python을 건드리지 않습니다.

```bash
# 1. pipx 설치 (없는 경우)
brew install pipx        # macOS
# 또는
apt install pipx         # Ubuntu/Debian
# 또는
pip install --user pipx  # 기타

# PATH 설정
pipx ensurepath

# 2. paper-assist 설치
pipx install paper-assist

# 3. 에이전트 등록 (한 번만 실행)
paper-assist install --global

# 4. 설치 확인
paper-assist status
```

**설치 후 사용 방법:**
```bash
# 어디서든 CLI 사용 가능
paper-assist extract paper.pdf
paper-assist equations paper.pdf

# Claude Code에서 에이전트 사용 (venv 불필요!)
claude
> @paper-assist 이 논문을 분석해 주세요
```

### pip로 설치

#### macOS (PEP 668 환경)

macOS는 시스템 Python 보호 정책으로 가상환경이 필요합니다:

```bash
# 가상환경 생성 및 활성화
python3 -m venv ~/.paper-assist-venv
source ~/.paper-assist-venv/bin/activate

# 설치
pip install paper-assist

# 에이전트 등록 (venv 활성화 상태에서)
paper-assist install --global
```

> **참고**: 에이전트(`@paper-assist`)는 한 번 등록하면 venv 없이도 Claude Code에서 사용 가능합니다.
> CLI 도구(`paper-assist extract` 등)는 venv 활성화가 필요합니다.

#### Linux/Windows

```bash
# 직접 설치 가능
pip install paper-assist

# 에이전트 등록
paper-assist install --global
```

### 소스에서 설치

```bash
git clone https://github.com/Hyuk0816/paper-assist-agent.git
cd paper-assist-agent

# pipx로 설치
pipx install .

# 또는 venv로 설치
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 설치 확인

```bash
# CLI 버전 확인
paper-assist --version

# 에이전트 설치 상태 확인
paper-assist status
```

**설치 위치:**
- 글로벌 에이전트: `~/.claude/agents/paper-assist.md`
- 로컬 에이전트: `./.claude/agents/paper-assist.md`

---

## 프로젝트 초기화

새 연구 프로젝트에서 PaperAssist를 사용하려면:

```bash
# 현재 디렉토리에 프로젝트 구조 생성
paper-assist init

# 또는 특정 경로에 생성
paper-assist init --path /path/to/my-research
```

### 생성되는 디렉토리 구조

```
PaperAssist/
│
├── current_draft/                     # 📍 GitHub (논문 초안)
│   ├── main.md                        # 논문 본문 (통합)
│   ├── sections/                      # 섹션별 분리
│   │   ├── 01_introduction.md
│   │   ├── 02_related_work.md
│   │   ├── 03_methodology.md
│   │   ├── 04_experiments.md
│   │   └── 05_conclusion.md
│   └── bibliography.bib               # 참고문헌 (BibTeX)
│
├── references/
│   ├── PDF/                           # 📍 Google Drive (원본 PDF)
│   │   └── YYYYMMDD_Author_Title.pdf
│   └── parsed/                        # 📍 GitHub (추출 결과)
│       ├── YYYYMMDD_Author_Title_text.txt
│       └── YYYYMMDD_Author_Title_equations.md
│
├── logs/                              # 📍 GitHub (모든 로그)
│   ├── analysis/                      # 논문 분석 로그
│   │   └── YYYYMMDD_Author_Title.md
│   ├── session/                       # 세션 로그
│   │   └── YYYYMMDD_session.md
│   └── decisions/                     # 의사결정 로그
│       └── YYYYMMDD_decision_topic.md
│
└── .claude/
    └── agents/
        └── paper-assist.md            # 에이전트 정의 (로컬 설치 시)
```

---

## 사용법

### Claude Code에서 에이전트 사용

Claude Code CLI에서 `@paper-assist`로 에이전트를 호출합니다:

#### 기본 논문 분석

```
@paper-assist 이 논문을 분석해 주세요: references/PDF/20260205_Vaswani_Transformer.pdf
```

에이전트가 수행하는 작업:
1. 디렉토리 구조 확인 및 생성
2. PDF에서 텍스트 추출
3. PDF에서 수식 추출 (LaTeX)
4. 섹션별 상세 분석
5. 인용 가치 판단
6. 분석 로그 생성
7. GitHub 커밋 및 푸시
8. Google Drive PDF 백업 (MCP 설치 시)

#### 비교 분석

```
@paper-assist 이 논문을 내 초안과 비교해서 분석해 주세요
```

#### 기존 분석 검색

```
@paper-assist attention 관련해서 분석했던 논문들 찾아줘
```

#### 특정 섹션 상세 분석

```
@paper-assist 이 논문의 Methodology 섹션을 더 자세히 설명해줘
```

#### 꼬리 질문 (대화형 스터디)

```
@paper-assist 이 수식에서 softmax를 왜 사용하는 거야?
```

```
@paper-assist 이 방법론이 내 연구랑 어떻게 다른 거야?
```

### CLI 직접 사용

에이전트 없이 CLI로 직접 사용할 수도 있습니다:

```bash
# PDF에서 텍스트 추출
paper-assist extract references/PDF/paper.pdf
paper-assist extract references/PDF/paper.pdf -o output.txt

# PDF에서 수식 추출 (LaTeX)
paper-assist equations references/PDF/paper.pdf
paper-assist equations references/PDF/paper.pdf -o equations.md

# 논문과 초안 비교
paper-assist compare references/parsed/paper_text.txt current_draft/main.md
```

---

## 파일 명명 규칙

모든 파일은 **`YYYYMMDD_Author_Title`** 형식을 따릅니다.

### 형식 설명

- **YYYYMMDD**: 분석 날짜 (예: 20260205)
- **Author**: 첫 번째 저자의 성 (예: Vaswani, Kim, Lee)
- **Title**: 논문 제목의 핵심 키워드 1-2개 (예: Transformer, BERT, GPT)

### 파일 유형별 예시

| 유형 | 형식 | 예시 |
|------|------|------|
| **PDF 원본** | `YYYYMMDD_Author_Title.pdf` | `20260205_Vaswani_Transformer.pdf` |
| **분석 로그** | `YYYYMMDD_Author_Title.md` | `20260205_Vaswani_Transformer.md` |
| **텍스트 추출** | `YYYYMMDD_Author_Title_text.txt` | `20260205_Vaswani_Transformer_text.txt` |
| **수식 추출** | `YYYYMMDD_Author_Title_equations.md` | `20260205_Vaswani_Transformer_equations.md` |
| **세션 로그** | `YYYYMMDD_session.md` | `20260205_session.md` |

### 명명 규칙의 장점

- **날짜별 정렬**: 언제 어떤 논문을 분석했는지 한눈에 파악
- **검색 용이**: 저자명이나 키워드로 빠른 검색
- **GitHub/Google Drive 동기화**: 동일한 이름으로 양쪽에서 관리

---

## 분석 로그 구조

PaperAssist는 **섹션 기반 분석**을 수행합니다.

### 분석 원칙

1. **섹션 기반**: 논문의 구조를 파악하고 각 섹션별로 요약
2. **중요 섹션 선별**: 문제 해결 및 실험에 직결되는 섹션은 상세히 분석
3. **유연한 구조**: 논문마다 섹션 구조가 다르므로 실제 논문에 맞게 조정

### 섹션별 중요도

| 중요도 | 섹션 | 분석 깊이 |
|--------|------|----------|
| **필수** | Abstract, Introduction, Methodology, Experiments, Conclusion | 상세 분석 |
| **선택** | Related Work, Discussion, Limitations | 핵심만 요약 |
| **참조** | Appendix, Acknowledgments | 필요시 언급 |

### 로그 구조 예시

```markdown
# 📄 논문 분석: Attention Is All You Need

## 📑 섹션별 분석

### Abstract
- 문제: RNN/CNN 기반 시퀀스 모델의 병렬화 한계
- 방법: Self-attention 기반 Transformer 아키텍처 제안
- 결과: 영어-독일어 번역 SOTA, 학습 시간 대폭 단축

### 1. Introduction
#### 1.1 문제 정의
순차적 계산의 병렬화 제약...

#### 1.2 기존 방법의 한계
- RNN: 순차 처리로 인한 병렬화 불가
- CNN: 장거리 의존성 학습에 많은 레이어 필요

#### 1.3 제안 방법 (핵심 아이디어)
Attention만으로 시퀀스 변환 수행...

### 3. Methodology ⭐ (상세)
#### 3.3 주요 수식
**Scaled Dot-Product Attention**
$$
\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$
- 의미: Query와 Key의 유사도를 계산하여 Value를 가중합
- 역할: 시퀀스 내 모든 위치 간의 관계를 직접 모델링

### 4. Experiments ⭐ (상세)
#### 4.2 주요 결과
| Model | EN-DE BLEU | EN-FR BLEU |
|-------|------------|------------|
| Transformer (big) | **28.4** | **41.0** |

### 🏷️ 인용 가치: Must 🔴 (0.85)
Transformer 기반 연구의 필수 인용 대상
```

---

## 인용 가치 판단

### 등급 기준

| 등급 | 점수 | 의미 | 판단 기준 |
|------|------|------|-----------|
| 🔴 **Must** | ≥ 0.7 | 필수 인용 | 핵심 방법론, 직접적 관련성, 분야 기초 논문 |
| 🟡 **Optional** | 0.4-0.7 | 선택적 인용 | 관련 기법, 비교 대상, 배경 지식 |
| ⚪ **Avoid** | < 0.4 | 인용 불필요 | 관련성 낮음, 더 나은 대안 존재 |

### 판단 요소

| 요소 | 가중치 | 설명 |
|------|--------|------|
| 키워드 중첩도 | 40% | 내 초안과의 키워드 유사도 |
| 방법론 유사성 | 30% | 접근 방식의 유사성 |
| 인용 지수 | 20% | 피인용 수, 학술적 영향력 |
| 학회 티어 | 10% | 발표 학회/저널의 수준 |

### 학회/저널 티어

| 티어 | 점수 | 학회/저널 |
|------|------|----------|
| **A*** | 1.0 | NeurIPS, ICML, ICLR, CVPR, ICCV, ACL, EMNLP, Nature, Science |
| **A** | 0.8 | AAAI, IJCAI, ECCV, NAACL, COLING, TPAMI, JMLR |
| **B** | 0.6 | WACV, BMVC, CoNLL, TACL, Pattern Recognition |
| **C** | 0.4 | 기타 peer-reviewed venues |

---

## 하이브리드 저장소

PaperAssist는 **GitHub**와 **Google Drive**를 함께 사용하는 하이브리드 저장소 구조를 권장합니다.

### 저장소 분리 원칙

| 저장소 | 저장 대상 | 이유 |
|--------|----------|------|
| **GitHub** | 텍스트, 로그, 추출 결과, 초안 | 버전 관리, 검색, 변경 이력 |
| **Google Drive** | PDF 원본 | 대용량 파일, 백업, 날짜별 기록 |

### 동기화 워크플로우

```
논문 분석 시작
       │
       ├── PDF 저장: Google Drive/PaperAssist/references/PDF/
       │
       ├── 텍스트 추출: GitHub repo/references/parsed/
       │
       ├── 수식 추출: GitHub repo/references/parsed/
       │
       ├── 분석 로그: GitHub repo/logs/analysis/
       │
       └── 자동 커밋/푸시: GitHub
```

### 장점

1. **PDF 용량 문제 해결**: GitHub의 대용량 파일 제한 우회
2. **날짜별 기록**: 언제 어떤 논문을 봤는지 양쪽에서 추적 가능
3. **검색 용이**: GitHub에서 로그 내용 검색, Drive에서 PDF 원본 확인
4. **백업**: 두 곳에 분산 저장으로 안전

---

## MCP 서버 연동

PaperAssist는 MCP(Model Context Protocol) 서버와 연동하여 더 강력한 기능을 제공합니다.

### 필수 MCP

**없음** - 기본 기능은 MCP 없이도 동작합니다.

### 권장 MCP

#### GitHub MCP

분석 로그를 자동으로 커밋/푸시합니다.

```json
// ~/.claude/settings.json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your-github-token"
      }
    }
  }
}
```

#### Google Drive MCP

PDF 원본을 자동으로 Google Drive에 백업합니다.

```json
// ~/.claude/settings.json
{
  "mcpServers": {
    "gdrive": {
      "command": "npx",
      "args": ["-y", "@anthropic/server-gdrive"]
    }
  }
}
```

### MCP 없이 사용

MCP가 없어도 Git 명령어와 수동 백업으로 동일한 워크플로우를 수행할 수 있습니다:

```bash
# Git 수동 커밋/푸시
git add logs/ references/parsed/
git commit -m "📝 Add analysis: Vaswani 2017 - Transformer"
git push origin main

# Google Drive 수동 업로드
# references/PDF/ 폴더를 Google Drive에 수동으로 동기화
```

---

## CLI 명령어

### 전체 명령어 목록

```bash
paper-assist --help
```

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `extract` | PDF에서 텍스트 추출 | `paper-assist extract paper.pdf` |
| `equations` | PDF에서 수식 추출 | `paper-assist equations paper.pdf` |
| `compare` | 논문과 초안 비교 | `paper-assist compare paper.txt draft.md` |
| `install` | 에이전트 설치 | `paper-assist install --global` |
| `uninstall` | 에이전트 제거 | `paper-assist uninstall --all` |
| `status` | 설치 상태 확인 | `paper-assist status` |
| `init` | 프로젝트 초기화 | `paper-assist init` |

### 명령어 상세

#### extract

```bash
# 기본 사용 (자동 출력 경로)
paper-assist extract references/PDF/paper.pdf
# 출력: references/parsed/paper_text.txt

# 출력 경로 지정
paper-assist extract paper.pdf -o /path/to/output.txt
```

#### equations

```bash
# 기본 사용 (LaTeX 형식)
paper-assist equations references/PDF/paper.pdf
# 출력: references/parsed/paper_equations.md

# 출력 경로 지정
paper-assist equations paper.pdf -o equations.md
```

#### compare

```bash
# 논문 텍스트와 초안 비교
paper-assist compare references/parsed/paper_text.txt current_draft/main.md

# 출력 경로 지정
paper-assist compare paper.txt draft.md -o comparison.md
```

#### install / uninstall

```bash
# 글로벌 설치 (권장)
paper-assist install
paper-assist install --global

# 로컬 설치 (현재 프로젝트만)
paper-assist install --local

# 글로벌 제거
paper-assist uninstall

# 모두 제거
paper-assist uninstall --all
```

#### init

```bash
# 현재 디렉토리에 초기화
paper-assist init

# 특정 경로에 초기화
paper-assist init --path /path/to/project
```

---

## 의존성

### 필수 의존성

| 패키지 | 버전 | 용도 |
|--------|------|------|
| Python | >= 3.10 | 런타임 |
| PyMuPDF | >= 1.23.0 | PDF 텍스트 추출 |
| click | >= 8.0.0 | CLI 프레임워크 |
| scikit-learn | >= 1.3.0 | 텍스트 비교 (TF-IDF) |

### 선택 의존성

| 패키지 | 버전 | 용도 |
|--------|------|------|
| pix2tex | >= 0.1.0 | PDF 수식 → LaTeX 변환 |

### 설치 확인

```bash
# 의존성 확인
pip list | grep -E "pymupdf|click|scikit-learn|pix2tex"

# pix2tex 설치 (수식 추출 기능 사용 시)
pip install pix2tex
```

---

## 문제 해결

### 자주 발생하는 문제

#### 1. "command not found: paper-assist"

**원인**: PATH에 pip 설치 경로가 없음

**해결**:
```bash
# pip 설치 경로 확인
python -m site --user-base

# PATH에 추가 (~/.bashrc 또는 ~/.zshrc)
export PATH="$PATH:$(python -m site --user-base)/bin"
```

#### 2. 에이전트가 인식되지 않음

**원인**: 에이전트가 설치되지 않았거나 잘못된 위치에 있음

**해결**:
```bash
# 설치 상태 확인
paper-assist status

# 재설치
paper-assist uninstall --all
paper-assist install
```

#### 3. PDF 텍스트 추출 실패

**원인**: 이미지 기반 PDF (스캔본)

**해결**:
- OCR이 필요한 PDF는 현재 지원하지 않음
- 텍스트 기반 PDF를 사용하거나, OCR 처리 후 사용

#### 4. 수식 추출이 작동하지 않음

**원인**: pix2tex가 설치되지 않음

**해결**:
```bash
pip install pix2tex
```

#### 5. Git 푸시 실패

**원인**: 원격 저장소 설정 안 됨 또는 권한 문제

**해결**:
```bash
# 원격 저장소 확인
git remote -v

# 원격 저장소 추가
git remote add origin https://github.com/username/repo.git

# 수동 푸시
git push -u origin main
```

#### 6. Google Drive MCP 연결 안 됨

**원인**: MCP 서버가 설정되지 않음

**해결**:
- MCP 설정은 선택 사항입니다
- 수동으로 Google Drive에 PDF를 업로드해도 됩니다
- MCP 설정 방법은 [MCP 서버 연동](#mcp-서버-연동) 섹션 참조

### 로그 확인

문제 발생 시 자세한 로그 확인:

```bash
# CLI 상세 출력
paper-assist extract paper.pdf --verbose

# Python 오류 추적
python -c "from paper_assist import extract_text; extract_text('paper.pdf')"
```

---

## 기여

이슈와 PR을 환영합니다!

### 개발 환경 설정

```bash
# 저장소 클론
git clone https://github.com/Hyuk0816/paper-assist-agent.git
cd paper-assist-agent

# 개발 의존성 설치
pip install -e ".[dev]"

# 테스트 실행
pytest
```

### 코드 스타일

```bash
# 포매팅
black src/

# 린팅
ruff check src/
```

---

## 라이선스

MIT License

---

## 관련 링크

- [Claude Code 문서](https://docs.anthropic.com/claude-code)
- [MCP 서버 목록](https://github.com/anthropics/mcp-servers)
- [pix2tex (LaTeX OCR)](https://github.com/lukas-blecher/LaTeX-OCR)
- [PyMuPDF 문서](https://pymupdf.readthedocs.io/)