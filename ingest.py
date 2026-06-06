import os
import uuid

import chromadb

from pypdf import PdfReader

from chromadb.utils.embedding_functions import (
    SentenceTransformerEmbeddingFunction
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

DATA_FOLDER = "data"
DB_PATH = "chroma_db"

embedding_function = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(
    path=DB_PATH
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)


def get_collection():

    return client.get_or_create_collection(
        name="documents",
        embedding_function=embedding_function
    )


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


def index_single_pdf(
    pdf_path,
    collection
):

    filename = os.path.basename(pdf_path)

    pages = extract_pdf_text(pdf_path)

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

            documents.append(chunk)

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

    return len(documents)


def rebuild_database():

    try:
        client.delete_collection(
            name="documents"
        )
    except:
        pass

    collection = get_collection()

    total_chunks = 0

    if not os.path.exists(
        DATA_FOLDER
    ):
        return 0

    for filename in os.listdir(
        DATA_FOLDER
    ):

        if filename.lower().endswith(
            ".pdf"
        ):

            pdf_path = os.path.join(
                DATA_FOLDER,
                filename
            )

            total_chunks += index_single_pdf(
                pdf_path,
                collection
            )

    print(
        f"Indexed {total_chunks} chunks"
    )

    return total_chunks


if __name__ == "__main__":

    rebuild_database()