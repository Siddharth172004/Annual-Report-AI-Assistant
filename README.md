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


