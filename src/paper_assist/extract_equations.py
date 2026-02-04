"""
PDF 수식 추출 모듈 (LaTeX 변환)
"""

import io
from pathlib import Path
from typing import Optional, List, Dict, Any

import fitz  # PyMuPDF

# pix2tex는 선택적 의존성으로 처리
try:
    from pix2tex.cli import LatexOCR
    PIX2TEX_AVAILABLE = True
except ImportError:
    PIX2TEX_AVAILABLE = False


def extract_equations(
    pdf_path: str,
    output_path: Optional[str] = None,
    format: str = 'latex'
) -> str:
    """PDF에서 수식을 추출합니다.

    Args:
        pdf_path: PDF 파일 경로
        output_path: 출력 파일 경로 (None이면 자동 생성)
        format: 출력 형식 ('latex' 또는 'mathml')

    Returns:
        출력 파일 경로
    """
    pdf_path = Path(pdf_path).resolve()

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")

    # 출력 경로 결정
    if output_path:
        output_path = Path(output_path).resolve()
    else:
        parsed_dir = pdf_path.parent.parent / 'parsed'
        parsed_dir.mkdir(parents=True, exist_ok=True)
        output_path = parsed_dir / f"{pdf_path.stem}_equations.md"

    # 수식 추출
    equations = _extract_equations_from_pdf(pdf_path, format)

    # 마크다운 형식으로 저장
    content = _format_equations_markdown(equations, pdf_path.name)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding='utf-8')

    return str(output_path)


def _extract_equations_from_pdf(pdf_path: Path, format: str) -> List[Dict[str, Any]]:
    """PDF에서 수식 이미지를 찾아 LaTeX로 변환합니다."""
    equations = []

    if not PIX2TEX_AVAILABLE:
        # pix2tex가 없으면 텍스트 기반 수식만 추출
        return _extract_text_equations(pdf_path)

    # pix2tex 모델 로드
    model = LatexOCR()

    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc, 1):
            # 페이지에서 이미지 추출
            images = page.get_images()

            for img_index, img in enumerate(images):
                try:
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]

                    # 이미지를 PIL로 변환
                    from PIL import Image
                    image = Image.open(io.BytesIO(image_bytes))

                    # 수식 이미지인지 휴리스틱하게 판단
                    # (작은 이미지이고 텍스트가 적은 경우)
                    if _is_likely_equation(image):
                        latex = model(image)
                        if latex and len(latex) > 2:
                            equations.append({
                                'page': page_num,
                                'index': img_index,
                                'latex': latex,
                                'type': 'image'
                            })
                except Exception:
                    continue

            # 텍스트 기반 수식도 추출 (인라인 수식)
            text_equations = _extract_inline_equations(page.get_text())
            for eq in text_equations:
                eq['page'] = page_num
                equations.append(eq)

    return equations


def _extract_text_equations(pdf_path: Path) -> List[Dict[str, Any]]:
    """텍스트에서 수식 패턴을 추출합니다 (pix2tex 없이)."""
    import re
    equations = []

    # LaTeX 수식 패턴
    patterns = [
        (r'\$\$(.+?)\$\$', 'display'),  # 디스플레이 수식
        (r'\$(.+?)\$', 'inline'),        # 인라인 수식
        (r'\\begin\{equation\}(.+?)\\end\{equation\}', 'equation'),
        (r'\\begin\{align\}(.+?)\\end\{align\}', 'align'),
    ]

    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc, 1):
            text = page.get_text()

            for pattern, eq_type in patterns:
                matches = re.finditer(pattern, text, re.DOTALL)
                for match in matches:
                    latex = match.group(1).strip()
                    if latex:
                        equations.append({
                            'page': page_num,
                            'latex': latex,
                            'type': eq_type
                        })

    return equations


def _extract_inline_equations(text: str) -> List[Dict[str, Any]]:
    """텍스트에서 인라인 수식을 추출합니다."""
    import re
    equations = []

    # 간단한 수학 표현 패턴
    patterns = [
        (r'\$(.+?)\$', 'inline'),
        (r'\\(.+?)\\', 'escaped'),
    ]

    for pattern, eq_type in patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            latex = match.group(1).strip()
            if latex and len(latex) > 1:
                equations.append({
                    'latex': latex,
                    'type': eq_type
                })

    return equations


def _is_likely_equation(image) -> bool:
    """이미지가 수식일 가능성을 판단합니다."""
    width, height = image.size

    # 너무 크거나 너무 작은 이미지는 제외
    if width > 1000 or height > 500:
        return False
    if width < 20 or height < 10:
        return False

    # 가로로 긴 이미지는 수식일 가능성이 높음
    aspect_ratio = width / height
    if 0.5 < aspect_ratio < 10:
        return True

    return False


def _format_equations_markdown(equations: List[Dict[str, Any]], filename: str) -> str:
    """추출된 수식을 마크다운 형식으로 포맷합니다."""
    lines = [
        f"# 수식 추출 결과: {filename}",
        "",
        f"총 {len(equations)}개의 수식이 추출되었습니다.",
        "",
    ]

    for i, eq in enumerate(equations, 1):
        page = eq.get('page', '?')
        eq_type = eq.get('type', 'unknown')
        latex = eq.get('latex', '')

        lines.append(f"## 수식 {i} (페이지 {page}, {eq_type})")
        lines.append("")
        lines.append("```latex")
        lines.append(latex)
        lines.append("```")
        lines.append("")
        lines.append(f"$$")
        lines.append(latex)
        lines.append(f"$$")
        lines.append("")

    return '\n'.join(lines)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("사용법: python extract_equations.py <pdf_path> [output_path]")
        sys.exit(1)

    pdf_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    result = extract_equations(pdf_file, output_file)
    print(f"수식 추출 완료: {result}")