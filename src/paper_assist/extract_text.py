"""
PDF 텍스트 추출 모듈
"""

from pathlib import Path
from typing import Optional

import fitz  # PyMuPDF


def extract_text(pdf_path: str, output_path: Optional[str] = None) -> str:
    """PDF에서 텍스트를 추출합니다.

    Args:
        pdf_path: PDF 파일 경로
        output_path: 출력 파일 경로 (None이면 자동 생성)

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
        # 기본: references/parsed/ 디렉토리에 저장
        parsed_dir = pdf_path.parent.parent / 'parsed'
        parsed_dir.mkdir(parents=True, exist_ok=True)
        output_path = parsed_dir / f"{pdf_path.stem}_text.txt"

    # PDF 텍스트 추출
    text_content = []

    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc, 1):
            text = page.get_text()
            if text.strip():
                text_content.append(f"--- Page {page_num} ---\n{text}")

    # 파일 저장
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text('\n\n'.join(text_content), encoding='utf-8')

    return str(output_path)


def extract_text_to_string(pdf_path: str) -> str:
    """PDF에서 텍스트를 문자열로 추출합니다.

    Args:
        pdf_path: PDF 파일 경로

    Returns:
        추출된 텍스트
    """
    pdf_path = Path(pdf_path).resolve()

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")

    text_content = []

    with fitz.open(pdf_path) as doc:
        for page in doc:
            text = page.get_text()
            if text.strip():
                text_content.append(text)

    return '\n\n'.join(text_content)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("사용법: python extract_text.py <pdf_path> [output_path]")
        sys.exit(1)

    pdf_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    result = extract_text(pdf_file, output_file)
    print(f"텍스트 추출 완료: {result}")