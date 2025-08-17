# Financial Data Explorer (Excel/PDF + LangChain + Vector DB)

## Features

- Upload Excel or PDF files with financial data.
- Automatic data extraction and chunking.
- Semantic search and Q&A with LangChain + vector DB.
- View and export extracted/processed data.

## Getting Started

1. Install requirements:
    ```
    pip install -r requirements.txt
    ```

2. Set your OpenAI API key:
    ```
    export OPENAI_API_KEY=your_openai_api_key
    ```

3. Run the app:
    ```
    streamlit run app.py
    ```

## Customization

- Extend `load_file()` to handle more file types or smarter parsing.
- Add your own financial analytics in the Q&A or post-processing steps.
- Swap in another vector DB (Pinecone, Qdrant, etc) if desired.
