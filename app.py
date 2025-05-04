import streamlit as st
from streamlit_chat import message
from streamlit_modal import Modal
from utils.auth import check_auth, login_form
from utils.pdf_utils import process_multiple_pdfs
from utils.vector_store import get_vector_store, search_similar_chunks
from utils.gemini_chat import get_gemini_response
from utils.feedback import log_feedback

# Set up the page configuration
st.set_page_config(page_title="📄 PDF Chatbot", layout="wide")

# Initialize Modal for Document Summary
modal = Modal(key="Demo Key", title="📄 Document Summary")

# Session State Initialization (Ensure persistence across reruns)
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pending_query" not in st.session_state:
    st.session_state.pending_query = None
if "pdf_chunks" not in st.session_state:
    st.session_state.pdf_chunks = None
if "uploaded_pdf_names" not in st.session_state:
    st.session_state.uploaded_pdf_names = []

# Authenticate the user
def authenticate_user():
    """Handle user authentication."""
    if not check_auth():
        login_form()
        st.stop()

# Load Custom CSS
def load_custom_css():
    """Load custom CSS for styling."""
    with open("styles/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Handle PDF Upload
def process_uploaded_pdfs(uploaded_pdfs):
    """Process uploaded PDFs and convert them into chunks."""
    if uploaded_pdfs:
        uploaded_names = [pdf.name for pdf in uploaded_pdfs]
        # Re-process only if new files are uploaded
        if uploaded_names != st.session_state.uploaded_pdf_names:
            with st.spinner("Processing new PDFs..."):
                chunks = process_multiple_pdfs(uploaded_pdfs)
                st.session_state.vector_store = get_vector_store(chunks)
                st.session_state.pdf_chunks = chunks
                # DO NOT reset chat history!
                st.session_state.uploaded_pdf_names = uploaded_names
            st.toast("PDFs processed. Start chatting!", icon="✅")

# Generate Document Summary
def generate_document_summary():
    """Generate and display a semantic summary of the uploaded PDFs."""
    if st.session_state.pdf_chunks:
        # Combine all text from chunks into a single string
        full_text = "\n\n".join([chunk["text"] for chunk in st.session_state.pdf_chunks])

        # Construct a better structured prompt
        prompt = f"""
                You are an expert summarizer. The user has uploaded a document and wants a clear summary of its contents.

                Please provide a semantic summary of the following text. Use bullet points or a section-wise breakdown if possible.
                If the document is long, prioritize summarizing key themes, structure, and important details.

                Document Content:
                {full_text[:8000]}  # Keep prompt within Gemini's token limits
                """

        # Call Gemini with the updated prompt
        summary = get_gemini_response(prompt)

        # Display the summary in a modal
        if summary:
            with modal.container():
                st.markdown(summary)


# Display Chatbot UI
def display_chat_interface():
    """Display the chat interface and handle user inputs."""
    st.title("📄 Chat with your PDFs using Gemini")

    # Display chat history
    if st.session_state.vector_store:
        for i, chat in enumerate(st.session_state.chat_history):
            is_user = chat["role"] == "user"
            message(chat["content"], is_user=is_user, key=f"chat_{i}")

            if not is_user:
                # Feedback buttons
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

                # Show sources for the assistant's response
                with st.expander(f"📄 Sources for this answer"):
                    for r in chat["sources"]:
                        st.markdown(f"📄 **{r['source']}** | Page {r['page']}\n> {r['text'][:300]}...")

    # User input field
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

            # Format the chunks nicely
            formatted_chunks = "\n\n".join([
                f"Source: {chunk['source']} | Page: {chunk['page']}\n{chunk['text']}"
                for chunk in results
            ])

            # Construct a detailed prompt
            prompt = f"""
            You are an expert assistant helping users understand a PDF document.

            Based on the following relevant excerpts from the PDF, answer the user's question as accurately and helpfully as possible.

            User's Question: {st.session_state.pending_query}

            Relevant Chunks:
            {formatted_chunks}

            Please provide a clear and concise answer. Cite sources if helpful.
            """

            # Pass the custom prompt to Gemini
            response = get_gemini_response(prompt)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response,
            "question": st.session_state.pending_query,
            "sources": results
        })

        st.session_state.pending_query = None
        st.rerun()

# Main execution flow
def main():
    """Main function to run the Streamlit app."""
    # Authentication check
    authenticate_user()

    # Load custom CSS
    load_custom_css()

    # Sidebar PDF upload
    st.sidebar.header("📂 Upload your PDFs")
    uploaded_pdfs = st.sidebar.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

    # Process uploaded PDFs
    process_uploaded_pdfs(uploaded_pdfs)

    # Generate Summary Button
    if uploaded_pdfs and st.sidebar.button("🧠 Generate Summary"):
        generate_document_summary()

    # Display the chat interface
    display_chat_interface()

# Run the app
if __name__ == "__main__":
    main()
