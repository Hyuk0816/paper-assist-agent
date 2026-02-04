"""
논문 비교 분석 모듈
"""

from pathlib import Path
from typing import Optional, Dict, Any, List
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compare_papers(
    paper_path: str,
    draft_path: str,
    output_path: Optional[str] = None
) -> str:
    """논문과 초안을 비교 분석합니다.

    Args:
        paper_path: 참조 논문 텍스트 파일 경로
        draft_path: 사용자 초안 파일 경로
        output_path: 출력 파일 경로 (None이면 자동 생성)

    Returns:
        출력 파일 경로
    """
    paper_path = Path(paper_path).resolve()
    draft_path = Path(draft_path).resolve()

    if not paper_path.exists():
        raise FileNotFoundError(f"논문 파일을 찾을 수 없습니다: {paper_path}")
    if not draft_path.exists():
        raise FileNotFoundError(f"초안 파일을 찾을 수 없습니다: {draft_path}")

    # 출력 경로 결정
    if output_path:
        output_path = Path(output_path).resolve()
    else:
        output_path = Path.cwd() / 'logs' / 'analysis' / f"comparison_{paper_path.stem}.md"

    # 텍스트 로드
    paper_text = paper_path.read_text(encoding='utf-8')
    draft_text = draft_path.read_text(encoding='utf-8')

    # 비교 분석 수행
    analysis = _analyze_comparison(paper_text, draft_text, paper_path.name, draft_path.name)

    # 결과 저장
    content = _format_comparison_report(analysis)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding='utf-8')

    return str(output_path)


def _analyze_comparison(
    paper_text: str,
    draft_text: str,
    paper_name: str,
    draft_name: str
) -> Dict[str, Any]:
    """두 텍스트를 비교 분석합니다."""

    # 텍스트 전처리
    paper_clean = _preprocess_text(paper_text)
    draft_clean = _preprocess_text(draft_text)

    # TF-IDF 유사도 계산
    similarity = _calculate_similarity(paper_clean, draft_clean)

    # 키워드 추출
    paper_keywords = _extract_keywords(paper_clean)
    draft_keywords = _extract_keywords(draft_clean)

    # 공통 키워드 및 차이점
    common_keywords = set(paper_keywords) & set(draft_keywords)
    paper_unique = set(paper_keywords) - set(draft_keywords)
    draft_unique = set(draft_keywords) - set(paper_keywords)

    # 인용 가치 점수 계산
    citation_score = _calculate_citation_score(similarity, common_keywords, paper_keywords)

    return {
        'paper_name': paper_name,
        'draft_name': draft_name,
        'similarity': similarity,
        'citation_score': citation_score,
        'citation_grade': _get_citation_grade(citation_score),
        'paper_keywords': paper_keywords[:20],
        'draft_keywords': draft_keywords[:20],
        'common_keywords': list(common_keywords)[:15],
        'paper_unique_keywords': list(paper_unique)[:10],
        'draft_unique_keywords': list(draft_unique)[:10],
        'paper_length': len(paper_text.split()),
        'draft_length': len(draft_text.split()),
    }


def _preprocess_text(text: str) -> str:
    """텍스트를 전처리합니다."""
    # 소문자 변환
    text = text.lower()
    # 특수문자 제거 (알파벳, 숫자, 공백만 유지)
    text = re.sub(r'[^a-z0-9가-힣\s]', ' ', text)
    # 연속 공백 제거
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def _calculate_similarity(text1: str, text2: str) -> float:
    """두 텍스트의 TF-IDF 코사인 유사도를 계산합니다."""
    try:
        vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(float(similarity), 4)
    except Exception:
        return 0.0


def _extract_keywords(text: str, top_n: int = 30) -> List[str]:
    """텍스트에서 주요 키워드를 추출합니다."""
    try:
        vectorizer = TfidfVectorizer(
            max_features=top_n * 2,
            stop_words='english',
            ngram_range=(1, 2)
        )
        tfidf_matrix = vectorizer.fit_transform([text])
        feature_names = vectorizer.get_feature_names_out()
        scores = tfidf_matrix.toarray()[0]

        # 점수로 정렬
        keyword_scores = list(zip(feature_names, scores))
        keyword_scores.sort(key=lambda x: x[1], reverse=True)

        return [kw for kw, score in keyword_scores[:top_n] if score > 0]
    except Exception:
        return []


def _calculate_citation_score(
    similarity: float,
    common_keywords: set,
    paper_keywords: List[str]
) -> float:
    """인용 가치 점수를 계산합니다.

    점수 기준:
    - 유사도 (40%): 텍스트 유사성
    - 키워드 중복률 (40%): 공통 키워드 비율
    - 논문 품질 추정 (20%): 키워드 다양성
    """
    # 유사도 점수 (0-1)
    similarity_score = min(similarity * 1.5, 1.0)  # 약간 스케일 조정

    # 키워드 중복률 (0-1)
    if paper_keywords:
        overlap_ratio = len(common_keywords) / len(paper_keywords)
    else:
        overlap_ratio = 0.0

    # 품질 추정 (키워드 수 기반)
    quality_score = min(len(paper_keywords) / 20, 1.0)

    # 가중 평균
    final_score = (
        similarity_score * 0.4 +
        overlap_ratio * 0.4 +
        quality_score * 0.2
    )

    return round(final_score, 2)


def _get_citation_grade(score: float) -> Dict[str, str]:
    """인용 가치 등급을 반환합니다."""
    if score >= 0.7:
        return {
            'grade': 'Must',
            'emoji': '🔴',
            'description': '필수 인용 - 핵심 방법론 제공, 직접적 관련성'
        }
    elif score >= 0.4:
        return {
            'grade': 'Optional',
            'emoji': '🟡',
            'description': '선택적 인용 - 관련 기법 소개, 비교 대상'
        }
    else:
        return {
            'grade': 'Avoid',
            'emoji': '⚪',
            'description': '인용 불필요 - 관련성 낮음, 더 나은 대안 존재'
        }


def _format_comparison_report(analysis: Dict[str, Any]) -> str:
    """비교 분석 결과를 마크다운 형식으로 포맷합니다."""
    grade = analysis['citation_grade']

    report = f"""# 논문 비교 분석 결과

## 비교 대상

| 항목 | 내용 |
|------|------|
| 참조 논문 | {analysis['paper_name']} |
| 사용자 초안 | {analysis['draft_name']} |
| 논문 길이 | {analysis['paper_length']} 단어 |
| 초안 길이 | {analysis['draft_length']} 단어 |

## 유사도 분석

| 지표 | 값 |
|------|------|
| 텍스트 유사도 | {analysis['similarity']:.2%} |
| 인용 가치 점수 | {analysis['citation_score']:.2f} |

## 인용 가치 판단

### 등급: {grade['grade']} {grade['emoji']}

**점수**: {analysis['citation_score']:.2f} / 1.00

**판단**: {grade['description']}

## 키워드 분석

### 공통 키워드 (관련성 지표)
{', '.join(analysis['common_keywords']) if analysis['common_keywords'] else '공통 키워드 없음'}

### 논문 고유 키워드 (참고 가치)
{', '.join(analysis['paper_unique_keywords']) if analysis['paper_unique_keywords'] else '없음'}

### 초안 고유 키워드 (차별점)
{', '.join(analysis['draft_unique_keywords']) if analysis['draft_unique_keywords'] else '없음'}

## 활용 권장 사항

"""

    if grade['grade'] == 'Must':
        report += """- ✅ **Related Work** 섹션에 반드시 포함
- ✅ 방법론 비교 분석에 활용
- ✅ 핵심 수식 및 개념 인용 권장
"""
    elif grade['grade'] == 'Optional':
        report += """- 🔶 **Related Work** 섹션에 선택적 포함
- 🔶 특정 기법 비교 시 참조
- 🔶 배경 지식 제공 용도로 활용
"""
    else:
        report += """- ⚪ 인용 우선순위 낮음
- ⚪ 더 관련성 높은 논문 검색 권장
- ⚪ 필요시 각주 또는 부록에서 언급
"""

    report += """
---
*이 분석은 Scholar-Sync에 의해 자동 생성되었습니다.*
"""

    return report


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("사용법: python compare_papers.py <paper_path> <draft_path> [output_path]")
        sys.exit(1)

    paper_file = sys.argv[1]
    draft_file = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else None

    result = compare_papers(paper_file, draft_file, output_file)
    print(f"비교 분석 완료: {result}")