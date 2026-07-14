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

    elif file_path.lower().endswith(".docx"):

        doc = Document(file_path)

        return "\n".join(
            paragraph.text
            for paragraph in doc.paragraphs
            if paragraph.text.strip()
        )

    return ""


def analyze_document(text: str) -> str:

    if not text.strip():

        return "Не вдалося прочитати текст документа."

    return (
        "📄 Документ успішно прочитано.\n\n"
        f"Символів: {len(text)}\n"
        f"Слів: {len(text.split())}"
    )