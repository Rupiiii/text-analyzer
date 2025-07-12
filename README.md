# Personal Knowledge Base Assistant using Gemini and FAISS (RAG)

This repository contains the implementation of a Personal Knowledge Base Assistant powered by Retrieval-Augmented Generation (RAG) using Google Gemini 1.5 Flash and FAISS. It allows you to query your own documents (PDF/text) and get intelligent, context-aware responses.

---

## Features

- Retrieval-Augmented Generation (RAG): Combines semantic search over your documents with generative AI responses.
- Google Gemini 1.5 Flash: Fast, intelligent LLM via the official `google-generativeai` SDK.
- FAISS and Sentence Transformers: Efficient similarity search using `faiss-cpu` and `MiniLM` embeddings.
- PDF Support: Automatically extracts and chunks content from PDF files.

---

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key: https://makersuite.google.com/app/apikey

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/personal-knowledge-base-assistant.git
   cd personal-knowledge-base-assistant
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Set your Gemini API key:
   You can either:
      1) Replace "your-api-key" directly in the code
      2) Or use an environment variable:

      ```bash
      export GEMINI_API_KEY="your-api-key"

---

### How It Works

1) Extracts text from your uploaded PDF file.
2) Splits the text into chunks for embedding.
3) Generates semantic embeddings using MiniLM.
4) Stores embeddings in a FAISS index.
5) Retrieves top-matching chunks based on your question.
6) Sends context and question to Gemini and returns a generated answer.

---

### License

This project is licensed under the MIT License. 

