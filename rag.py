import os
import chromadb
import traceback

from dotenv import load_dotenv
from google import genai

import os

if not os.path.exists("chroma_db"):
    from ingest import rebuild_database
    rebuild_database()

load_dotenv()

# -----------------------

# Gemini Setup

# -----------------------

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found."
    )

client_gemini = genai.Client(
api_key=GEMINI_API_KEY
)

# -----------------------

# ChromaDB Setup

# -----------------------

client = chromadb.PersistentClient(
path="chroma_db"
)

from chromadb.utils.embedding_functions import (
    SentenceTransformerEmbeddingFunction
)

embedding_function = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

def get_collection():

    return client.get_or_create_collection(
        name="documents",
        embedding_function=embedding_function
    )

# -----------------------

# RAG Function

# -----------------------

def answer_question(
question,
selected_document=None
):
    """
    Answers a question using a Retrieval-Augmented Generation (RAG) approach by querying a ChromaDB collection
    and generating a response with Gemini, optionally filtering by a selected document.

    Parameters:
        question (str): The user's question to answer.
        selected_document (str, optional): The name of the document to restrict the search to. If None or "All Documents", searches all documents.

    Returns:
        dict: A dictionary containing the answer, sources, similarity scores, and retrieved document chunks.
    """

    try:

        collection = get_collection()

        # Search

        if (
            selected_document
            and selected_document !=
            "All Documents"
        ):

            results = collection.query(
                query_texts=[question],
                n_results=10,
                where={
                    "source": selected_document
                }
            )

        else:

            results = collection.query(
                query_texts=[question],
                n_results=10
            )

        # Check if results are empty
        if not results.get("documents") or not results["documents"][0]:
            return {
                "answer": "No relevant documents found.",
                "sources": [],
                "scores": [],
                "chunks": []
            }

        retrieved_docs = results["documents"][0]

        metadatas = (
            results["metadatas"][0]
            if results.get("metadatas") and len(results["metadatas"]) > 0
            else []
        )

        distances_list = results.get("distances", [[]])
        if distances_list and len(distances_list) > 0:
            distances = distances_list[0]
        else:
            distances = []

        # Context

        context = "\n\n".join(
            retrieved_docs
        )

        prompt = f"""
You are an expert document assistant.

Rules:

1. Answer ONLY from the provided context.
2. Do not use outside knowledge.
3. If the answer is unavailable, say:
   'I cannot find the answer in the provided documents.'
4. Give detailed answers.
5. Use bullet points when useful.

Context:
{context}

Question:
{question}
"""


        # Gemini

        response = (
            client_gemini
            .models
            .generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
        )

        answer = response.text

        # Sources

        sources = []
        scores = []

        for i, meta in enumerate(
            metadatas
        ):

            sources.append(
                {
                    "Source":
                    meta.get(
                        "source",
                        "Unknown"
                    ),
                    "Page":
                    meta.get(
                        "page",
                        "-"
                    )
                }
            )

            if i < len(
                distances
            ):

                similarity = round(
                    (
                        1 -
                        distances[i]
                    ) * 100,
                    2
                )

                scores.append(
                    {
                        "Similarity (%)":
                        similarity
                    }
                )

        return {

            "answer":
            answer,

            "sources":
            sources,

            "scores":
            scores,

            "chunks":
            retrieved_docs
        }

except Exception as e:

    return {

        "answer":
        f"{type(e).__name__}: {str(e)}\n\n{traceback.format_exc()}",

        "sources": [],
        "scores": [],
        "chunks": []
    }

