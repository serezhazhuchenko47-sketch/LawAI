import pdfplumber
from docx import Document


def extract_text(file_path: str) -> str:
    """
    Зчитує текст із PDF або DOCX.
    """

    if file_path.lower().endswith(".pdf"):

        text = ""

        with pdfplumber.open(file_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text.strip()

    if file_path.lower().endswith(".docx"):

        doc = Document(file_path)

        paragraphs = []

        for paragraph in doc.paragraphs:

            if paragraph.text.strip():
                paragraphs.append(paragraph.text)

        return "\n".join(paragraphs)

    return ""


def analyze_document(text: str) -> str:
    """
    Базовий аналіз документа.
    """

    text = text.strip()

    if not text:

        return "Не вдалося прочитати текст документа."

    words = len(text.split())

    return (
        "📄 Документ успішно прочитано.\n\n"
        f"Символів: {len(text)}\n"
        f"Слів: {words}"
    )