import streamlit as st
import pandas as pd
from langchain.document_loaders import UnstructuredExcelLoader, PDFMinerLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

# Choose between Excel or PDF loader
def load_file(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        loader = PDFMinerLoader(uploaded_file)
    elif uploaded_file.name.endswith((".xls", ".xlsx")):
        loader = UnstructuredExcelLoader(uploaded_file)
    else:
        st.error("Unsupported file format.")
        return None
    return loader.load_and_split()

st.title("Financial Data Explorer (Excel/PDF + LangChain + Vector DB)")
uploaded_file = st.file_uploader("Upload an Excel or PDF file", type=["pdf", "xls", "xlsx"])

if uploaded_file:
    # Step 1: Load and chunk data
    docs = load_file(uploaded_file)
    if docs is None:
        st.stop()
    st.success(f"Loaded {len(docs)} document chunks.")

    # Step 2: Create embeddings and store in Chroma vector DB (in-memory for demo)
    embeddings = OpenAIEmbeddings()
    db = Chroma.from_documents(docs, embeddings)
    st.info("Data indexed in vector database.")

    # Step 3: Interactive Q&A via LangChain
    llm = OpenAI(temperature=0)
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())
    user_query = st.text_input("Ask a question about your data (e.g., 'Show me net profit for 2023'):")

    if user_query:
        response = qa.run(user_query)
        st.write("**Answer:**", response)

    # Step 4: Data exploration & export
    if st.button("Show Raw Extracted Data"):
        # For demo: Collect all text chunks
        all_chunks = [d.page_content for d in docs]
        st.write(all_chunks)

    if st.button("Export Extracted Data as CSV"):
        # For demo: Save all text chunks to CSV
        df = pd.DataFrame({"chunk": [d.page_content for d in docs]})
        csv = df.to_csv(index=False)
        st.download_button("Download CSV", csv, "extracted_data.csv")
