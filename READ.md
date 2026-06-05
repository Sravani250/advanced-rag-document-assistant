# Advanced RAG Document Q&A Assistant

## Overview

This project is an AI-powered Document Question Answering Assistant built using Retrieval-Augmented Generation (RAG). The application allows users to upload PDF documents, create a searchable knowledge base, and ask natural language questions about the uploaded content.

Instead of searching documents manually, users can interact with the system through a simple chat-like interface and receive accurate answers generated from the information available in the uploaded PDFs.

The system combines semantic search using vector embeddings with Google's Gemini model to provide context-aware responses while displaying the sources used to generate the answer.

---

## Problem Statement

Organizations, students, and researchers often work with large PDF documents such as reports, research papers, resumes, technical documentation, and financial statements.

Finding specific information inside these documents can be time-consuming.

This project solves that problem by allowing users to ask questions directly and receive answers based on the contents of the uploaded documents.

---

## Features

### Document Management

* Upload PDF documents
* Store documents in a centralized knowledge base
* View available PDFs within the application

### Intelligent Search

* Semantic document retrieval using embeddings
* Search across multiple PDF documents
* Retrieve the most relevant content chunks

### AI-Powered Question Answering

* Context-aware answer generation using Gemini
* Answers generated only from retrieved document content
* Reduced hallucinations through Retrieval-Augmented Generation

### Transparency & Explainability

* Display source documents used
* Show page references
* Display retrieved text chunks
* Similarity score visualization

### User Experience

* Interactive Streamlit interface
* Chat history support
* Suggested question prompts
* Knowledge base overview dashboard

---

## System Architecture

```text
PDF Documents
      │
      ▼
Text Extraction (PyPDF)
      │
      ▼
Text Chunking
      │
      ▼
Vector Embeddings
      │
      ▼
ChromaDB Vector Store
      │
      ▼
Semantic Retrieval
      │
      ▼
Gemini LLM
      │
      ▼
Generated Answer
```

---

## Technologies Used

### Frontend

* Streamlit

### Backend

* Python

### AI & NLP

* Google Gemini API
* Sentence Transformers

### Vector Database

* ChromaDB

### Document Processing

* PyPDF

### Text Processing

* LangChain Text Splitters

---

## Project Workflow

### Step 1: Upload Documents

Users upload PDF files through the application interface.

### Step 2: Text Extraction

The system extracts textual content from each page of the uploaded PDF.

### Step 3: Chunk Creation

Large text blocks are divided into smaller chunks to improve retrieval quality.

### Step 4: Vector Embedding Generation

Each chunk is converted into numerical vector representations using a transformer-based embedding model.

### Step 5: Storage in ChromaDB

The generated embeddings are stored in ChromaDB for efficient similarity search.

### Step 6: User Query

The user enters a natural language question.

### Step 7: Retrieval

The most relevant document chunks are retrieved from the vector database.

### Step 8: Answer Generation

Retrieved chunks are passed to Gemini, which generates a context-based answer.

### Step 9: Source Display

The application displays:

* Generated answer
* Source documents
* Page references
* Retrieved chunks
* Similarity scores

---

## Example Questions

### Resume-Based Questions

* What skills are mentioned in the resume?
* List the projects completed by the candidate.
* What certifications are available?
* What technologies does the candidate know?

### Financial Reports

* What are Apple's major sources of revenue?
* What sustainability initiatives are mentioned in Tesla's report?
* What risks are highlighted in the financial statements?

### AI Documents

* What AI products are discussed in the NVIDIA document?
* Summarize the NVIDIA AI portfolio.

---

## Project Structure

```text
rag-qa-bot/
│
├── app.py
├── ingest.py
├── rag.py
├── .env
├── requirements.txt
│
├── data/
│   ├── Apple Report.pdf
│   ├── Tesla Report.pdf
│   ├── NVIDIA Report.pdf
│   └── Resume.pdf
│
└── chroma_db/
```

---

## How to Run

### Clone the Repository

```bash
git clone <repository-link>
cd rag-qa-bot
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure API Key

Create a `.env` file and add:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

### Index Documents

```bash
python ingest.py
```

### Launch Application

```bash
streamlit run app.py
```

---

## Future Enhancements

* Automatic document indexing after upload
* OCR support for scanned PDFs
* Hybrid retrieval (Keyword + Semantic Search)
* Multi-document comparison
* Conversation memory
* PDF preview inside the application
* User authentication and document management
* Advanced reranking models for retrieval quality

---

## Learning Outcomes

Through this project, I gained practical experience in:

* Retrieval-Augmented Generation (RAG)
* Vector databases
* Embedding models
* Large Language Models (LLMs)
* Semantic search
* Streamlit application development
* Prompt engineering
* Document intelligence systems

---

## Conclusion

This project demonstrates how Retrieval-Augmented Generation can be used to transform static PDF documents into an interactive knowledge base. By combining semantic search with large language models, users can quickly obtain relevant information from multiple documents through natural language queries.

The solution improves accessibility, reduces manual document search effort, and provides a foundation for building enterprise-grade document intelligence applications.
