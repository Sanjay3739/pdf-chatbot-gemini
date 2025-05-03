import os
from dotenv import load_dotenv
import google.generativeai as genai

# ✅ Load environment variables from .env
load_dotenv()

# ✅ Get API key and model name from env
api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")  # fallback if missing

# ✅ Configure Gemini
genai.configure(api_key=api_key)

# ✅ Define response function
def get_gemini_response(query, chunks):
    context = "\n".join([c["text"] for c in chunks])
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text