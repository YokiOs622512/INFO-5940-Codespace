# Reference

## External sources and tools used
1. Steamlit: build an web-based chat interface
2. os: get API_KEY from environment variable
3. pypdf: read pdf files
4. langchain_text_splitters: split documents into small chunks
5. langchain_core.documents: format documents with their metadata
6. langchain.vectorstores: embed chunks and store
7. langchain_openai: initialize embedding and LLM models
8. langchain_core.messages: compose prompt sent to LLM model
9. chromadb: store embed vector

## GenAI usage
1. Use GenAI to understand the code in langgraph_chroma_retreiver.ipynb.
2. Use GenAI to understand the difference between langgraph and langchain.
3. Use GenAI to debug API error.
4. Use GenAI to fix grammar in ref-log.md and README.md.
5. Use GenAI to understand how to define the a good parameters number insides RecursiveCharacterTextSplitter() and as_retriever().