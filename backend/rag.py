import argparse
import os
import sys
from typing import List, Optional, Tuple
import chromadb
import google.generativeai as genai
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.schema import Document
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

CHROMA_PATH = "chroma"
DEFAULT_COLLECTION_NAME = "langchain"

def get_rag_response(query_text: str, tone: Optional[str] = None) -> Tuple[str, List[str]]:
    """
    Performs a RAG query and returns the response and sources.
    
    Args:
        query_text (str): The user's query.
        tone (Optional[str]): The desired tone for the response (e.g., "formal", "casual").
    
    Returns:
        Tuple[str, List[str]]: The generated response text and a list of source documents.
    """

    # Load the vector database with the pre-trained embeddings
    embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_function,
        collection_name=DEFAULT_COLLECTION_NAME
    )

    # k=3 retrieves the top 3 most similar documents to the user's query
    results: List[Document] = db.similarity_search_with_score(query_text, k=4)

    # Get the context from the retrieved documents
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    # Define the prompt template that gives the agent its context
    PROMPT_TEMPLATE = """
    You are acting as Qaanit Baderoen (Answer in first person).
    You have access to his professional, personal and academic documents. 
    Make your response sound human-like — avoid robotic phrasing and avoid greeting. Avoid using em dashes.
    When using information from the knowledge base, phrase it as if you're recalling it yourself.
    If you cannot find the answer in the provided context, politely say that you do not know (As if you were Qaanit).

    {tone_instruction}

    Context:
    {context}

    ---

    Question: {question}

    Respond in the first person, as if you are Qaanit.
    """

    tone_instruction = f"Provide your answer using a {tone} tone." if tone else ""
    
    # Format the prompt with the retrieved context and user's question
    prompt = PROMPT_TEMPLATE.format(tone_instruction=tone_instruction, context=context_text, question=query_text)

    # Initialize the LLM
    try:
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    except KeyError:
        print("Error: GOOGLE_API_KEY not found in environment variables.")
        print("Please set your API key in a .env file or as an environment variable.")
        sys.exit(1)

    llm = genai.GenerativeModel('gemini-1.5-flash-latest')

    # Generate the response
    response = llm.generate_content(prompt)
    sources = [doc.metadata.get('source') for doc, _score in results]

    return response.text, sources


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query the RAG system.")
    parser.add_argument("query_text", type=str, help="The text query to search for.")
    parser.add_argument("--tone", type=str, default=None, help="The desired tone for the response.")
    args = parser.parse_args()
    
    try:
        response_text, sources = get_rag_response(args.query_text, args.tone)
        print("Response:", response_text)
        print("\nSources:", sources)
    except (FileNotFoundError, ValueError, EnvironmentError) as e:
        print(f"Error: {e}")
