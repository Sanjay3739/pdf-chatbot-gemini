# 📄 Gemini-Powered PDF Chatbot (Streamlit App)

Talk with your PDF documents using Google Gemini, Streamlit, and vector search — with citations, sources, and feedback tracking. 🚀

---

## 📌 Features

- 🔐 User login & authentication
- 📚 Upload and process multiple PDFs
- 🤖 Chat with Gemini about your documents
- 🔍 Semantic search using vector embeddings
- 📄 Source viewing with page numbers and context
- 👍👎 Feedback buttons for response quality
- ⚡ Fast, interactive UI using Streamlit + streamlit_chat

---

## 🧠 Tech Stack

- Frontend: `Streamlit`, `streamlit_chat`
- Backend: `Google Gemini API`, `FAISS` (or other vector DB)
- NLP: Chunking, Embedding
- Auth: Custom login via `check_auth`
- PDF: `PyMuPDF`, `pdfminer`, or similar
- Feedback: Stored/logged locally or to DB

---

## 🔧 Setup Guide (Step-by-Step)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/pdf-chatbot-gemini.git
cd pdf-chatbot-gemini
```

### 2️⃣ Create and Activate Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables

```bash
GEMINI_API_KEY=your_google_gemini_key
GEMINI_MODEL=your_gemini_model_name
USER_NAME=your_name
PASSWORD=your_password
```

### 5️⃣ Project Structure Overview
```bash

├── app.py                    # Main Streamlit app
├── utils/
│   ├── auth.py              # Auth functions
│   ├── pdf_utils.py         # PDF processing & chunking
│   ├── vector_store.py      # Vector search setup (e.g., FAISS)
│   ├── gemini_chat.py       # Gemini API interaction
│   └── feedback.py          # Logging feedback
├── requirements.txt
├── .gitignore
└── README.md
```