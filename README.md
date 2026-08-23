# 🤖 RAG Document Chatbot

An AI-powered document question-answering system built using **Retrieval-Augmented Generation (RAG)**. Users can upload PDF or DOCX documents and ask questions based on the uploaded content.

The system retrieves the most relevant document chunks using vector similarity search and generates answers using a local LLM.

---

## 🚀 Features

- 📄 Upload PDF and DOCX documents
- 📝 Extract text from documents
- ✂️ Intelligent document chunking
- 🧠 Generate text embeddings using Sentence Transformers
- 🔎 Semantic similarity search using FAISS
- 🤖 Generate answers using Llama 3.2 through Ollama
- 💬 Ask natural-language questions about documents
- 🌐 Flask-based web interface
- 🔒 Answers are generated using retrieved document context

---

## 🏗️ RAG Architecture

```text
                    USER
                      │
                      ▼
              Upload PDF / DOCX
                      │
                      ▼
              Document Loader
                      │
                      ▼
                Text Extraction
                      │
                      ▼
                 Chunking
                      │
                      ▼
              Embedding Model
          (all-MiniLM-L6-v2)
                      │
                      ▼
                  FAISS
              Vector Database
                      │
                      │
              User Question
                      │
                      ▼
              Query Embedding
                      │
                      ▼
             Similarity Search
                      │
                      ▼
             Relevant Chunks
                      │
                      ▼
             Llama 3.2 (Ollama)
                      │
                      ▼
                  Answer
