from docx import Document
import PyPDF2
from io import BytesIO

def read_docx(file_stream):
    doc = Document(file_stream)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def read_pdf(file_stream):
    reader = PyPDF2.PdfReader(BytesIO(file_stream.read()))
    text = ""
    for page in reader.pages:
        text += page.extract_text() + '\n'
    return text
