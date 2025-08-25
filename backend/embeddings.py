# from langchain.document_loaders import DirectoryLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
# from langchain.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import chromadb
from chromadb.utils import embedding_functions
import openai 
from dotenv import load_dotenv
import os
import shutil


# Setting my API key
load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

# Initialize Chroma client (local persistent DB)
chroma_client = chromadb.PersistentClient(path="chroma_store")

# Use OpenAI for embeddings
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openai.api_key,
    model_name="text-embedding-3-small"
)

# Our main collection
collection = chroma_client.get_or_create_collection(
    name="personal_codex",
    embedding_function=openai_ef
)

def load_documents():
    categories = ["professional", "academic", "personal"]
    documents = []

    for c in categories:
        filePath = os.path.join("data", c)
        loader = DirectoryLoader(filePath, glob="*.md")
        doc = loader.load()
        documents += doc # this caused me lots of problems XD

    return documents

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300, # chosen for the relatively small size of the documents
        chunk_overlap=50,
        length_function=len,
        add_start_index=True,
    )

    
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    #document = chunks[10]
    #print(document.page_content)
    #print(document.metadata)

    return chunks

def main():
    docs = load_documents()
    chunks = split_text(docs)
    

if __name__ == "__main__":
    main()
    