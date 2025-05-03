import streamlit as st
from streamlit_chat import message
from utils.auth import check_auth, login_form
from utils.pdf_utils import process_multiple_pdfs
from utils.vector_store import get_vector_store, search_similar_chunks
from utils.gemini_chat import get_gemini_response
from utils.feedback import log_feedback

st.set_page_config(page_title="📄 PDF Chatbot", layout="wide")

# ✅ Auth check
if not check_auth():
    login_form()
    st.stop()

st.markdown("""
    <style>
    .stChatMessage {
        max-width: 700px !important;
    }
    .streamlit-expanderHeader {
        font-size: 0.9rem !important;
    }
    button[kind="secondary"] {
        padding: 0.25rem 0.6rem;
        font-size: 0.8rem;
        margin-right: 5px;
    }
    .st-emotion-cache-13na8ym   {
        width: 500px !important;
        word-wrap: break-word;
    }
</style>

""", unsafe_allow_html=True)

st.title("📄 Chat with your PDFs using Gemini")

# ✅ Sidebar PDF upload
st.sidebar.header("📂 Upload your PDFs")
uploaded_pdfs = st.sidebar.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

# ✅ Init session state
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pending_query" not in st.session_state:
    st.session_state.pending_query = None

# ✅ Process PDFs once
if uploaded_pdfs and st.session_state.vector_store is None:
    with st.spinner("Processing PDFs..."):
        chunks = process_multiple_pdfs(uploaded_pdfs)
        st.session_state.vector_store = get_vector_store(chunks)
    st.success("PDFs processed. Start chatting!")

# ✅ Display chat messages using fixed keys
if st.session_state.vector_store:
    for i, chat in enumerate(st.session_state.chat_history):
        is_user = chat["role"] == "user"
        message(chat["content"], is_user=is_user, key=f"chat_{i}")

        if not is_user:
            # ✅ Feedback buttons with 5px spacing (safe Streamlit layout)
            with st.container():
                col1, col2, spacer = st.columns([0.05, 0.05, 0.9])
                with col1:
                    if st.button("👍", key=f"pos_{i}"):
                        log_feedback(chat["question"], chat["content"], "positive")
                        st.toast("Thanks for your feedback!", icon="👍")
                with col2:
                    if st.button("👎", key=f"neg_{i}"):
                        log_feedback(chat["question"], chat["content"], "negative")
                        st.toast("We'll try to improve!", icon="🙏")

            # ✅ Show Sources with 500px width (using custom class)
            with st.expander(f"📄 Sources for this answer"):
                for r in chat["sources"]:
                    st.markdown(f"📄 **{r['source']}** | Page {r['page']}\n> {r['text'][:300]}...")
            
    # ✅ Chat input field
    query = st.chat_input("Ask a question...")

    # Step 1: Add user message and rerun
    if query and st.session_state.pending_query is None:
        st.session_state.chat_history.append({
            "role": "user",
            "content": query
        })
        st.session_state.pending_query = query
        st.rerun()

    # Step 2: If query pending, respond and rerun
    if st.session_state.pending_query:
        with st.spinner("Thinking..."):
            results = search_similar_chunks(st.session_state.pending_query, st.session_state.vector_store)
            response = get_gemini_response(st.session_state.pending_query, results)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response,
            "question": st.session_state.pending_query,
            "sources": results
        })

        st.session_state.pending_query = None
        st.rerun()
