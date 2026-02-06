# PaperAssist

**학술 논문 분석을 위한 Claude Code 에이전트**

PDF 논문에서 수식을 추출하고, 섹션별로 상세 분석하며, 인용 가치를 판단하고, 연구 로그를 자동으로 생성합니다.

---

## 설치

```bash
npx paper-assist
```

이 명령어 하나로 에이전트가 `~/.claude/agents/paper-assist.md`에 설치됩니다.

### 설치 확인

```bash
npx paper-assist status
```

### 제거

```bash
npx paper-assist uninstall
```

---

## 사용법

Claude Code에서 `@paper-assist`로 에이전트를 호출합니다:

```
@paper-assist 이 논문을 분석해 주세요: references/PDF/20260205_Vaswani_Transformer.pdf
```

### 주요 기능

| 기능 | 설명 |
|------|------|
| **PDF 분석** | Claude의 PDF 읽기 기능으로 논문 직접 분석 |
| **섹션별 상세 분석** | Methodology, Experiments 등 중요 섹션 상세 분석 |
| **인용 가치 판단** | Must / Optional / Avoid 등급으로 자동 분류 |
| **연구 로그 자동 생성** | 분석 결과를 마크다운으로 체계적 저장 |
| **Git 연동** | 분석 로그 자동 커밋/푸시 |

### 사용 예시

```
# 기본 분석
@paper-assist 이 논문을 분석해 주세요: paper.pdf

# 비교 분석
@paper-assist 이 논문을 내 초안과 비교해서 분석해 주세요

# 특정 섹션 상세 분석
@paper-assist 이 논문의 Methodology 섹션을 더 자세히 설명해줘

# 기존 분석 검색
@paper-assist attention 관련해서 분석했던 논문들 찾아줘
```

---

## 프로젝트 구조

에이전트가 생성/관리하는 디렉토리 구조:

```
PaperAssist/
├── references/
│   ├── PDF/                    # PDF 원본
│   └── parsed/                 # 추출 결과 (텍스트, 수식)
├── logs/
│   └── analysis/               # 논문 분석 로그
└── current_draft/              # 내 논문 초안 (비교 분석용)
```

---

## 인용 가치 판단

| 등급 | 점수 | 의미 |
|------|------|------|
| 🔴 **Must** | ≥ 0.7 | 필수 인용 (핵심 방법론, 직접적 관련성) |
| 🟡 **Optional** | 0.4-0.7 | 선택적 인용 (관련 기법, 배경 지식) |
| ⚪ **Avoid** | < 0.4 | 인용 불필요 (관련성 낮음) |

---

## 파일 명명 규칙

모든 파일은 `YYYYMMDD_Author_Title` 형식:

- `20260205_Vaswani_Transformer.pdf` (원본)
- `20260205_Vaswani_Transformer.md` (분석 로그)
- `20260205_Vaswani_Transformer_equations.md` (수식)

---

## 라이선스

MIT License
