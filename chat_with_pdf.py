import streamlit as st
import os
from pypdf import PdfReader # import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_core.documents import Document
from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

API_KEY = os.environ["API_KEY"]
BASE_URL = "https://api.ai.it.cornell.edu"

# Initialize LLM model
llm = ChatOpenAI(
    model="openai.gpt-4o",
    temperature=0.2,
    api_key = API_KEY,
    base_url = BASE_URL
)

# Initialize embedding model
embeddings = OpenAIEmbeddings(
    model = "openai.text-embedding-3-large", 
    api_key = API_KEY, 
    base_url = BASE_URL
)

def read_file(file):
    # A helper function to read .pdf, .txt, and .md files
    if file.name.lower().endswith(".pdf"): # Handle .pdf file
        # Create a pdf reader to read file and initialize the file_content to be used later
        pdf_reader = PdfReader(file)
        file_content = ""
        # Iteratively read the pdf file page by page if page is not None
        for page in pdf_reader.pages:
            page_content = page.extract_text()
            if page_content:
                file_content += page_content 
    else: # Handle .txt and .md file
        file_content = file.read().decode("utf-8")
    return file_content

def format_docs(docs):
    # A helper function to combine the most similar content
    return "\n\n---\n\n".join(d.page_content for d in docs)

st.title("📝 File Q&A with OpenAI")
# add the ability to upload multiple files, and user can upload pdf files as well
uploaded_file = st.file_uploader(
    "Upload one or more files", 
    type=("txt", "md", "pdf"), 
    accept_multiple_files = True
) 

# Get question from user
question = st.chat_input(
    "Ask something about the documents",
    disabled=not uploaded_file,
)

# Append assistant prompt to messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Ask something about the article"}]

# Iteratively write previous conversation
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])



if question and uploaded_file:
    # Append the user's question to the messages
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)
    # Read the content of the uploaded file
    if "uploaded_files_content" not in st.session_state:
        st.session_state["uploaded_files_content"] = {} # If user first time uploads files, create a dictionary "uploaded_files_content" to store the files
    # Iteratively read the uploaded files, and add to the dictionary with file name and content pair
    for file in uploaded_file:
        file_content = read_file(file)
        st.session_state["uploaded_files_content"][file.name] = file_content

    # Create a text_splitter with chunk_size = 1000 and chunk_overlap = 200
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )

    # Initialize all_chunk to store all documents that uploaded by the user so far later
    all_chunks = []
    # Iteratively split formatting file content and add to all_chunks file by file
    for file_name, content in st.session_state["uploaded_files_content"].items():
        content_format = [Document(page_content = content, metadata = {"source": file_name})]
        chunks = text_splitter.split_documents(content_format)
        all_chunks.extend(chunks)
        
    # Embedding all_chunks to a variable vectorstore
    vectorstore = Chroma.from_documents(
        documents = all_chunks, 
        embedding = embeddings
    )
    
    # Create a retriever with search_type = "similarity", and return top 10 most similar content
    retriever = vectorstore.as_retriever(
        search_type="similarity", 
        search_kwargs={"k": 10}
    )
    
    # retreive relevant content and format it
    docs = retriever.invoke(question)
    similar_content = format_docs(docs)

    # Compose a system prompt
    system_instructions = (
    "You are a helpful assistant for question answering.\n"
    "Use ONLY the provided context to answer concisely (<=3 sentences).\n"
    "If the answer isn't in the context, say you don't know.\n\n"
    f"Context:\n{similar_content}"
    )

    # Use LLM to generate response
    response = llm.invoke([
        SystemMessage(content=system_instructions),
        HumanMessage(content=question),
    ])

    # Append the assistant's response to the messages
    st.session_state.messages.append({"role": "assistant", "content": response.content})
    st.chat_message("assistant").write(response.content)

    # Print response and source in terminal
    print("Answer:\n", response.content, "\n")
    print("Sources:")
    for i, d in enumerate(docs, 1):
        src = d.metadata.get("source", "(no source)")
        print(f"[{i}] {src}")
