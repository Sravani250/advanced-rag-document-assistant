import streamlit as st
import os

from rag import answer_question

st.set_page_config(
page_title="Advanced RAG Knowledge Assistant",
page_icon="📚",
layout="wide"
)

DATA_FOLDER = "data"

st.title("Advanced RAG Knowledge Assistant")

# -----------------------

# Chat History

# -----------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------

# Load PDFs

# -----------------------

pdf_files = []

if os.path.exists(DATA_FOLDER):
    pdf_files = [
        file
        for file in os.listdir(DATA_FOLDER)
        if file.lower().endswith(".pdf")
    ]


# -----------------------

# Dashboard

# -----------------------

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Documents",
        len(pdf_files)
    )

with col2:
    st.metric(
        "Embedding Model",
        "MiniLM-L6-v2"
    )

# -----------------------

# Knowledge Base

# -----------------------

st.subheader("Knowledge Base")

if pdf_files:
    for pdf in pdf_files:
        st.success(pdf)


else:
    st.warning(
        "No PDF documents found."
    )

# -----------------------

# Upload PDFs

# -----------------------

st.subheader("Upload New PDFs")

uploaded_files = st.file_uploader(
"Choose PDF Files",
type=["pdf"],
accept_multiple_files=True
)

if uploaded_files:

    os.makedirs(
        DATA_FOLDER,
        exist_ok=True
    )

uploaded_count = 0

for file in uploaded_files:

    save_path = os.path.join(
        DATA_FOLDER,
        file.name
    )

    if os.path.exists(save_path):

        st.warning(
            f"{file.name} already exists."
        )

        continue

    with open(
        save_path,
        "wb"
    ) as f:

        f.write(
            file.getbuffer()
        )

    uploaded_count += 1

if uploaded_count > 0:

    st.success(
        f"{uploaded_count} PDF(s) uploaded successfully."
    )

    st.info(
        "Run: python ingest.py"
    )

# -----------------------

# Search Mode

# -----------------------

st.subheader("Search Mode")

search_mode = st.radio(
"Choose Search Mode",
[
"All Documents",
"Specific Document"
]
)

selected_document = None

if (
search_mode
== "Specific Document"
):
    selected_document = (
        st.selectbox(
            "Select PDF",
            pdf_files
        )
    )




# Ask Question

# -----------------------

st.subheader("Ask a Question")

question = st.text_input(
    "Enter your question"
)

if st.button("Generate Answer"):
    if question.strip():
        with st.spinner("Generating answer..."):
            result = answer_question(
                question,
                selected_document
            )

        st.subheader("✅ Answer")
        st.write(result["answer"])

        st.subheader(" Sources")
        st.table(result["sources"])

        if result.get("scores"):
            st.subheader(" Similarity Scores")
            st.table(result["scores"])

        st.subheader(" Retrieved Chunks")
        for i, chunk in enumerate(result["chunks"], start=1):
            with st.expander(f"Chunk {i}"):
                st.write(chunk)

        st.session_state.chat_history.append(
            {
                "question": question,
                "answer": result["answer"]
            }
        )


# -----------------------

# Chat History

# -----------------------

if st.session_state.chat_history:
    st.subheader(
        " Chat History"
    )

    for item in reversed(
        st.session_state.chat_history
    ):
        with st.expander(
            item["question"]
        ):
            st.write(
                item["answer"]
            )
