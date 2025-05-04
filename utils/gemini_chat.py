import os
from dotenv import load_dotenv
import google.generativeai as genai

# ✅ Load environment variables from .env file
load_dotenv()

# ✅ Get API key and model name from environment variables
api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")  # fallback to "gemini-1.5-flash" if GEMINI_MODEL is missing

# ✅ Check if API key is available
if not api_key:
    raise ValueError("API key for Gemini is missing. Please set GEMINI_API_KEY in the .env file.")

# ✅ Configure Gemini with API key
genai.configure(api_key=api_key)

# ✅ Initialize the Gemini model once at the beginning
model = genai.GenerativeModel(model_name)

# ✅ Define response function
def get_gemini_response(query, chunks):
    """
    Generates a response from the Gemini model using the provided query and context.
    """
    context = "\n".join([c["text"] for c in chunks])  # Combine context chunks into a single string
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    
    try:
        response = model.generate_content(prompt)  # Get response from Gemini model
        return response.text
    except Exception as e:
        print(f"Error generating response from Gemini: {e}")  # Handle potential errors
        return "Sorry, there was an error while generating the response. Please try again later."
