import google.generativeai as genai

genai.configure(api_key="AIzaSyCzuYU3ljMc1X7Q5KgAf5rGZvBp_TCl7RU")

def get_gemini_response(query, chunks):
    context = "\n".join([c["text"] for c in chunks])
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text