# main.py

import os
import sys
import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware # Import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# Add the parent directory to the system path to allow imports from embeddings.py and rag.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the necessary functions from your other scripts
from embeddings import CHROMA_PATH, embed_single_file
from rag import get_rag_response

ALLOW_ORIGIN = os.getenv("ALLOW_ORIGIN", "*")

# Define the FastAPI app
app = FastAPI(
    title="RAG Agent API",
    description="API for a Retrieval-Augmented Generation agent.",
    version="1.0.0",
)

# --- CORS Configuration ---
# Your frontend (http://localhost:5173) is a different origin,
# so we need to tell the backend to allow requests from it.
origins = [
    #"http://localhost:5173",  # The URL of your React development server
    "https://qaanitgpt-jn7o5h47f-qaanit-baderoens-projects.vercel.app/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Pydantic model to define the request body structure
class QueryRequest(BaseModel):
    """
    Model for the incoming user query and optional tone.
    """
    query: str
    tone: Optional[str] = None  # Added tone parameter

class RAGResponse(BaseModel):
    """
    Model for the outgoing response.
    """
    response_text: str
    sources: List[str]

# --- API Endpoints ---

@app.get("/")
def read_root():
    """
    Root endpoint to verify the API is running.
    """
    return {"message": "RAG Agent API is running!"}

@app.post("/query", response_model=RAGResponse)
async def query_agent(request: QueryRequest):
    """
    Endpoint to process a user query using the RAG agent.

    Args:
        request (QueryRequest): The incoming request containing the user's query and tone.

    Returns:
        RAGResponse: The generated response and the list of sources.
    
    Raises:
        HTTPException: If the ChromaDB directory is not found.
    """
    # Check if the ChromaDB directory exists before attempting to query it
    if not os.path.exists(CHROMA_PATH):
        raise HTTPException(
            status_code=500,
            detail=f"The ChromaDB directory at '{CHROMA_PATH}' was not found. Please run `python embeddings.py` first."
        )

    try:
        # Pass both the query and tone to the RAG logic
        response_text, sources = get_rag_response(request.query, request.tone)
        
        # Return the response as a JSON object
        return RAGResponse(response_text=response_text, sources=sources)

    except Exception as e:
        # Handle any other unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the query: {str(e)}"
        )
    


@app.post("/upload")
async def upload_file(category: str = Form(...), file: UploadFile = File(...)):
    """
    Upload a file, save to local category folder, and embed into ChromaDB.
    """
    valid_categories = ["professional", "academic", "personal"]
    if category not in valid_categories:
        raise HTTPException(status_code=400, detail=f"Invalid category. Choose from {valid_categories}.")

    save_dir = os.path.join("data", category)
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, file.filename)

    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Embed and add to Chroma
        embed_single_file(file_path, category)
        return {"message": f"File '{file.filename}' uploaded and embedded under {category}."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

# --- Uvicorn Server Command ---
# To run this file, save it as main.py and execute the following command in your terminal:
# uvicorn main:app --reload

# The `--reload` flag is useful for development as it automatically
# reloads the server when code changes are detected.
