# Retrieval Augmented Generation (RAG) Application using Langchain in Streamlit

This application implements **Retrieval Augmented Generation (RAG)** system using Streamlit, LangChain, and Chromadb to let user to upload multiple ".txt", ".md", and ".pdf" files, and asking questions regarding the files.

## Instruction to Run the Application

This repository is designed to run in Codespace. The Codespace will build the environment which define in "devcontainer" and "requirement.txt" automatically. To run the application, run the following code in Codespace terminal.

STEP 1: Set the API Key
```bash
export API_KEY="your_API_KEY"
```
STEP 2: Call Streamlit to run your program
```bash
streamlit run chat_with_pdf.py
```
or you can do STEP 1 and STEP 2 together with
```bash
API_KEY="your_API_KEY" streamlit run chat_with_pdf.py
```

To run the application locally, run this line of code in the terminal before STEP 1 and STEP 2 above.
```bash
pip install -r requirements.txt
```

## Project Feature
1. Upload, extract, and chunk multiple files (".txt", ".md", ".pdf").
2. Embed document chunks into vector and store in a Chromadb variable.
3. Retrieve relevant information from embedded document.
4. Use LLM to generate responses based on the retrieved chunks.
5. Use st.session_state to maintain conversation history for multiple runs.

## Pipeline of the Application
1. Document Loading: use read_file() to extract text from uploaded files.
2. Chunking: use RecursiveCharacterTextSplitter to chunk the files into small chunks.
3. Embedding: use Chroma.from_documents to embed chunks and store in Chromadb variable.
4. Retrieving: use a retriever with similarity search to return most relevant chunks.
5. Augmenting: pass the relevant information and user's question to LLM to get answers.
6. Generating: display the answer in streamlit chat interface.

## requirement.txt update
1. Add langchain-text-splitters for split document into chunks
2. Add chromadb for store embedding vector