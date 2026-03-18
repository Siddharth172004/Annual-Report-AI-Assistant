# 📊 Annual Report AI Assistant

![Python](https://img.shields.io/badge/Python-3.10-blue)
![LangChain](https://img.shields.io/badge/LangChain-Framework-green)
![OCR](https://img.shields.io/badge/OCR-Tesseract-orange)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen)

---

## 🚀 Overview

Annual Report AI Assistant is built on real official **2024–25 annual reports** of HDFC Bank, ICICI Bank, and Reliance (RIL).

It uses a **Hybrid RAG approach (Text + OCR)**:

- First, full PDF text is extracted and converted into embeddings  
- Then, all pages are converted into images → OCR is applied → embeddings are generated  

This ensures accurate results even for **scanned content, charts, and PPTs**, improving overall context understanding and answer quality.

It combines:
- 📄 Text Extraction  
- 🖼️ OCR Processing  
- 🧠 Embeddings + Vector Search  
- 🤖 LLM-based Answer Generation  

---

## 🔄 RAG Pipeline Flow

```
                📄 PDF Documents
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
   Text Extraction                PDF → Images → OCR
        │                               │
        └───────────────┬───────────────┘
                        ▼
                   Chunking
                        │
                        ▼
                   Embeddings
                        │
                        ▼
                Vector Database (FAISS)
                        │
                        ▼
                   User Query
                        │
                        ▼
                Query Embedding
                        │
                        ▼
               Similarity Search
                        │
                        ▼
              Top Relevant Chunks
                        │
                        ▼
                 Context Creation
                        │
                        ▼
            LLM (Gemini / OpenAI)
                        │
                        ▼
                   Final Answer

⚡ Hybrid RAG: Combines Text + OCR embeddings for better accuracy on real-world PDFs.

```
---

## 🔥 Core Features

- ✔ Handles scanned & non-scanned PDFs  
- ✔ Dual pipeline (Text + OCR) for maximum accuracy  
- ✔ Works on large-scale documents (1000+ pages)  
- ✔ Semantic search using embeddings  
- ✔ Context-aware AI responses  
- ✔ Real-world financial data understanding  

---

## 🧠 System Design

### 1️⃣ Text Embedding Pipeline
- Extract text from PDF  
- Split into chunks  
- Generate embeddings using Sentence Transformers  
- Store in vector database (FAISS)  

---

### 2️⃣ OCR Pipeline (Important)

- Convert PDF pages → images  
- Apply Tesseract OCR (PyTesseract)  
- Extract hidden / scanned text  
- Clean extracted text  
- Chunk + generate embeddings  
- Store in vector DB  

---

## 🖼️ OCR Setup (PyTesseract)

### 🔹 Step 1: Install Tesseract Engine

#### Windows:
- Download: https://github.com/UB-Mannheim/tesseract/wiki  
- Install it  
- Add path:


