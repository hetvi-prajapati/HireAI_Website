# ============================================================
#  TalentSync — DOCX Parser
#  Extracts raw text from Word documents using python-docx.
# ============================================================

import docx
from app.utils.logger import get_logger

logger = get_logger(__name__)

def extract_text_from_docx(file) -> str:
    """
    Extract text from a DOCX file object.
    """
    try:
        doc = docx.Document(file)
        full_text = []
        for para in doc.paragraphs:
            if para.text.strip():
                full_text.append(para.text.strip())
        return '\n'.join(full_text)
    except Exception as e:
        logger.error(f"Failed to parse DOCX: {str(e)}")
        return ""
