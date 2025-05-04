import fitz  # PyMuPDF
import spacy
nlp = spacy.load("en_core_web_sm")

# ✅ Extracts text from a PDF file and splits it into chunks of specified size
def extract_text_chunks(pdf_file, source_name, max_tokens=300):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    chunks = []

    for i, page in enumerate(doc):
        text = page.get_text()
        sentences = [sent.text for sent in nlp(text).sents]
        chunk = ""

        for sentence in sentences:
            if len(chunk.split()) + len(sentence.split()) <= max_tokens:
                chunk += " " + sentence
            else:
                chunks.append({"text": chunk.strip(), "page": i + 1, "source": source_name})
                chunk = sentence

        if chunk:
            chunks.append({"text": chunk.strip(), "page": i + 1, "source": source_name})

    return chunks

# ✅ Process multiple PDF files and extract chunks from each
def process_multiple_pdfs(pdf_files):
    all_chunks = []
    for pdf in pdf_files:
        all_chunks.extend(extract_text_chunks(pdf, pdf.name))
    return all_chunks
