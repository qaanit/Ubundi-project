# from langchain.document_loaders import DirectoryLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
# from langchain.embeddings import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
import chromadb
#from chromadb.utils import embedding_functions
#import openai 
from dotenv import load_dotenv
import os
import shutil


# Setting my API key
load_dotenv()
#openai.api_key = os.environ['OPENAI_API_KEY']

CHROMA_PATH = "chroma"
DEFAULT_COLLECTION_NAME = "langchain"


def load_documents():
    categories = ["professional", "personal", "academic"]
    documents = []

    for c in categories:
        filePath = os.path.join("data", c)
        loader = DirectoryLoader(filePath, glob="*.md")
        doc = loader.load()
        documents += doc # this caused me lots of problems XD

    return documents

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, # chosen for the relatively small size of the documents
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )

    
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    #document = chunks[10]
    #print(document.page_content)
    #print(document.metadata)

    return chunks


def save_to_chroma(chunks: list[Document]):
    # 1. Create a client to connect to the Chroma database
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    
    # 2. Try to get the collection. If it exists, we delete it.
    try:
        print(f"Clearing old data from collection: '{DEFAULT_COLLECTION_NAME}'")
        client.delete_collection(name=DEFAULT_COLLECTION_NAME)
    except chromadb.errors.NotFoundError:
        # This error is thrown if the collection does not exist, which is fine.
        print("Collection not found, creating a new one.")
        pass

    # Create a new DB from the documents.
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = Chroma.from_documents(
        chunks, embeddings, collection_name=DEFAULT_COLLECTION_NAME, persist_directory=CHROMA_PATH
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

def embed_single_file(file_path: str, category: str):
    """
    Embed a single new file and add it to ChromaDB without wiping the DB.
    """
    from langchain_community.document_loaders import TextLoader
    
    loader = TextLoader(file_path)
    documents = loader.load()

    chunks = split_text(documents)

    client = chromadb.PersistentClient(path=CHROMA_PATH)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Connect to existing collection
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings,
        collection_name=DEFAULT_COLLECTION_NAME
    )

    db.add_documents(chunks)
    db.persist()
    print(f"Added {len(chunks)} chunks from {file_path} to {CHROMA_PATH}.")


def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)
    print("Everything saved!")

def main():
    generate_data_store()
    

if __name__ == "__main__":
    main()
    