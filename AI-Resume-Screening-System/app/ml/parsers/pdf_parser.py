# ============================================================
#  TalentSync — PDF Resume Parser
#  Extracts raw text from PDF resume files using PyPDF2.
#  Swap extract_text_from_pdf() with pdfplumber for better
#  table/multi-column layout support when needed.
# ============================================================

import io
import PyPDF2
from app.utils.logger import get_logger

logger = get_logger(__name__)


def extract_text_from_pdf(file) -> str:
    """
    Extract all text from a PDF file object.

    Args:
        file: A file-like object (werkzeug FileStorage or raw bytes IO).

    Returns:
        str: Lowercase full-text content of the PDF.
             Returns empty string on failure.
    """
    try:
        # Ensure we're reading from the beginning
        if hasattr(file, 'seek'):
            file.seek(0)

        pdf_reader = PyPDF2.PdfReader(file)
        pages_text = []

        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            if page_text:
                pages_text.append(page_text)
            else:
                logger.warning(f"Page {page_num + 1} returned no text (may be image-based).")

        full_text = "\n".join(pages_text)
        logger.info(f"PDF parsed: {len(pdf_reader.pages)} pages, {len(full_text)} characters extracted.")
        return full_text.lower()

    except PyPDF2.errors.PdfReadError as e:
        logger.error(f"PyPDF2 read error: {e}")
        return ""
    except Exception as e:
        logger.error(f"Unexpected PDF parsing error: {e}")
        return ""


def extract_text_from_bytes(file_bytes: bytes) -> str:
    """Convenience wrapper: accepts raw bytes instead of a file object."""
    return extract_text_from_pdf(io.BytesIO(file_bytes))
