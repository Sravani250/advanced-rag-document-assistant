import os
import uuid

import chromadb

from pypdf import PdfReader

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

# -----------------------
# Configuration
# -----------------------

DATA_FOLDER = "data"
DB_PATH = "chroma_db"

# -----------------------
# ChromaDB
# -----------------------

client = chromadb.PersistentClient(
    path=DB_PATH
)

collection = client.get_or_create_collection(
    name="documents"
)

# -----------------------
# Text Splitter
# -----------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

# -----------------------
# PDF Extraction
# -----------------------

def extract_pdf_text(pdf_path):

    reader = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):

        text = page.extract_text()

        if text and text.strip():

            pages.append(
                {
                    "page": page_number,
                    "text": text
                }
            )

    return pages


# -----------------------
# Index Single PDF
# -----------------------

def index_single_pdf(pdf_path):

    filename = os.path.basename(
        pdf_path
    )

    print(
        f"Indexing: {filename}"
    )

    pages = extract_pdf_text(
        pdf_path
    )

    documents = []
    metadatas = []
    ids = []

    for page in pages:

        chunks = splitter.split_text(
            page["text"]
        )

        for chunk_no, chunk in enumerate(
            chunks,
            start=1
        ):

            documents.append(
                chunk
            )

            metadatas.append(
                {
                    "source": filename,
                    "page": page["page"],
                    "chunk": chunk_no
                }
            )

            ids.append(
                str(uuid.uuid4())
            )

    if documents:

        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    print(
        f"{len(documents)} chunks indexed."
    )

    return len(documents)


# -----------------------
# Rebuild Database
# -----------------------

def rebuild_database():

    global collection

    print(
        "Rebuilding database..."
    )

    try:

        client.delete_collection(
            name="documents"
        )

        print(
            "Old collection removed."
        )

    except Exception:

        pass

    collection = client.get_or_create_collection(
        name="documents"
    )

    total_chunks = 0

    if not os.path.exists(
        DATA_FOLDER
    ):

        print(
            "Data folder not found."
        )

        return 0

    pdf_files = [

        file

        for file in os.listdir(
            DATA_FOLDER
        )

        if file.lower().endswith(
            ".pdf"
        )
    ]

    for pdf in pdf_files:

        pdf_path = os.path.join(
            DATA_FOLDER,
            pdf
        )

        chunks = index_single_pdf(
            pdf_path
        )

        total_chunks += chunks

    print(
        f"\nSuccessfully indexed {total_chunks} chunks."
    )

    return total_chunks


# -----------------------
# Statistics
# -----------------------

def get_stats():

    try:

        count = collection.count()

        return {
            "chunks": count
        }

    except Exception:

        return {
            "chunks": 0
        }


# -----------------------
# Main
# -----------------------

if __name__ == "__main__":

    rebuild_database()
