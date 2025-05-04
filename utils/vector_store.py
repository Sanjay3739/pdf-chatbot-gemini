import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Create a vector store with embeddings for the given chunks
def get_vector_store(chunks):
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    return {"index": index, "chunks": chunks, "embeddings": embeddings}

# ✅ Search for the top k most similar chunks to a query
def search_similar_chunks(query, store, top_k=3):
    query_vec = model.encode([query])
    _, I = store["index"].search(query_vec, top_k)
    return [store["chunks"][i] for i in I[0]]
