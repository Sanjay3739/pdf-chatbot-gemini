import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_vector_store(chunks):
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    return {"index": index, "chunks": chunks, "embeddings": embeddings}


def search_similar_chunks(query, store, top_k=3):
    query_vec = model.encode([query])
    _, I = store["index"].search(query_vec, top_k)
    return [store["chunks"][i] for i in I[0]]
