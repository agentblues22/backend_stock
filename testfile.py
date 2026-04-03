import os
from huggingface_hub import InferenceClient
import requests
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# 🔐 NEVER hardcode tokens in real apps


# ✅ Step 1: Load PDF
loader = PyPDFLoader("resume.pdf")
documents = loader.load()

# ✅ Step 2: Split text
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=100
)
docs = text_splitter.split_documents(documents)

# ✅ Step 3: ✅ CORRECT embedding model (small)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"local_files_only":True}
)

# ✅ Step 4: Vector store
vectorstore = Chroma.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 7})



def ask_llm(context, question):
    prompt = f"""
You are a good AI agent. Don't overthink and explain the steps. Answer based ONLY on the context. If the answer isn't in the context, Reply "I don't Know"

Context:
{context}

Question:
{question}
"""

   
    url = "http://localhost:11434/api/generate"
    data = {
    "model": "phi:latest",
    "prompt": prompt,
    "stream": False,
    "options":{
        "num_predict":150
    }
}

    response = requests.post(url, json=data)

    return (response.json()["response"])

# ✅ Step 6: Query
query = "what is the users Marital Status?"

retrieved_docs = retriever.invoke(query)
context = "\n".join([doc.page_content for doc in retrieved_docs])

answer = ask_llm(context, query)

print(answer)