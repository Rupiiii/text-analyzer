import faiss
import numpy as np
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

# ---------- Configuration ----------

# Set your Gemini API key
genai.configure(api_key="GOOGLE_API_KEY")  # Replace this safely!

# Load the embedding model
embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# ---------- Functions ----------

def extract_text_from_pdf(pdf_path):
    """Extracts and concatenates text from all pages in the PDF."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

def split_text_into_chunks(text, chunk_size=500):
    """Splits text into word-based chunks."""
    words = text.split()
    chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

def generate_embeddings(chunks):
    """Generates embeddings for a list of text chunks."""
    embeddings = embedding_model.encode(chunks, convert_to_numpy=True)
    return embeddings

def store_embeddings_in_faiss(embeddings):
    """Stores the embeddings in a FAISS index."""
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    print(f"Stored {index.ntotal} embeddings in FAISS.")
    return index

def search_faiss(index, query, k=3):
    """Performs vector search using FAISS."""
    query_embedding = embedding_model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, k)
    return indices[0], distances[0]

def generate_response_with_gemini(query, index, chunks, k=3):
    """
    Uses Gemini 1.5 Flash to generate an answer based on relevant document chunks.
    """
    # Step 1: Retrieve top-k relevant chunks
    top_indices, _ = search_faiss(index, query, k=k)
    relevant_chunks = [chunks[i] for i in top_indices]

    # Step 2: Build context and prompt
    context = "\n".join(relevant_chunks)
    prompt = (
        f"You are a helpful assistant. Use the following context to answer the user's question.\n\n"
        f"Context:\n{context}\n\n"
        f"User Query:\n{query}\n\n"
        f"Answer:"
    )

    # Step 3: Call Gemini
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    response = model.generate_content(prompt)

    return response.text

# ---------- Main Execution ----------

if __name__ == "__main__":
    pdf_path = "YOUR.pdf"  # Replace with your actual PDF path

    # Step 1: Process PDF
    text = extract_text_from_pdf(pdf_path)
    chunks = split_text_into_chunks(text, chunk_size=300)

    # Step 2: Embedding & Indexing
    embeddings = generate_embeddings(chunks)
    index = store_embeddings_in_faiss(embeddings)

    # Step 3: Query
    query = "YOUR QUERY"
    answer = generate_response_with_gemini(query, index, chunks)

    print("\nGenerated Response:\n", answer)

