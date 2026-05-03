**Stock Market Analytics Dashboard — Backend**

A FastAPI backend powering real-time stock market analysis, featuring multi-source data aggregation, technical indicator calculation, and an AI agent for natural language market queries.
Features

-Multi-source API aggregation (price data, fundamentals, news)

-Technical indicators calculated from raw data — RSI, ROC, Moving Averages

-RAG-based AI agent powered by ChromaDB and HuggingFace

-RESTful API serving processed insights to the frontend

**Tech Stack**

FastAPI, ChromaDB, HuggingFace, Pandas, NumPy, PyPDF, Uvicorn

**Installation**

-bashpip install huggingface chroma fastapi requests pandas numpy pypdf uvicorn

**run**

-uvicorn main:app --reload

**Architecture**

Two primary routes handle all operations:
/ask — AI agent endpoint processing natural language queries via a RAG pipeline built with LangChain and  ChromaDB. A PDF document(finance_metrics_general_guide.pdf) serves as the knowledge base, providing contextual information that grounds the AI agent's responses.
/company — Data pipeline endpoint handling multi-source aggregation and transformation

*RAG Pipeline:*

PDF ingested and chunked as the context/knowledge source
Embeddings stored and retrieved via ChromaDB
LangChain orchestrates query processing and response generation
HuggingFace models power the embedding and generation layer

*Data Pipeline:*

Source 1: OHLC price data at 5-minute intervals
Source 2: Fundamental metrics (EPS, EBITDA)
Source 3: Latest news sentiment

Raw data is transformed into smoothed moving averages, RSI and ROC indicators before being served to the frontend.

**API Configuration**

Demo mode reads from a static CSV. To enable live data follow the instructions in code comments.
