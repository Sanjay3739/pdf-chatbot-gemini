import fitz  # PyMuPDF

def extract_text_chunks(pdf_file, source_name, chunk_size=500):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    chunks = []
    for i, page in enumerate(doc):
        text = page.get_text()
        for j in range(0, len(text), chunk_size):
            chunk_text = text[j:j+chunk_size]
            chunks.append({"text": chunk_text, "page": i+1, "source": source_name})
    return chunks

def process_multiple_pdfs(pdf_files):
    all_chunks = []
    for pdf in pdf_files:
        all_chunks.extend(extract_text_chunks(pdf, pdf.name))
    return all_chunks