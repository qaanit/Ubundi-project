# QaanitGPT – RAG Agent
#### QaanitGPT is a personal knowledge agent that uses FastAPI, ChromaDB, and Google Gemini embeddings to store and query personal, academic, and professional documents.
#### The frontend is built with React and deployed on Vercel, while the backend runs on Render.

#### This project acts as a digital extension of myself — able to answer questions in my voice by retrieving context from uploaded documents (Markdown files, CV, cover letters, personal writing, etc.).  

## ⚡ Where to find & how to use
Please visit my project at the link provided in my Github repo. Please ask me (the agent) any questions about my career/education/projects/background.
- ⚠️ **DO NOT UPLOAD ANY FILES WHATSOEVER**, this feature DOES work and the files will be added to the vector storage. This could drastically change the answers the agent produces. The feature was only added as a proof of concept.
- ⚠️ Please try not to ask TOO MANY questions too fast, as my API key only has a few (but enough for thorough testing) tokens.
- ⚠️ When asking a question for the first time, the backend will have to 'wake up'. You might get an error for your first query but send a second one and it will work correctly.

## 🚀 Features

- **File Upload & Categorization:** Upload documents directly in the frontend, assign them to categories (Academic, Professional, Personal).
- **Auto-Indexing with ChromaDB:** New files are embedded with Google Gemini embeddings and added to the vector database.
- **Semantic Search + RAG:** Queries retrieve relevant context from documents and feed into the LLM for human-like responses.
- **First-Person Responses:** Custom prompt template ensures responses sound like me, not an AI.
- **Fullstack Deployment:** React frontend (Vercel) + FastAPI backend (Render).

## 📂 Project structure
The project is set up with two seperate folders within the root folder: backend and frontend for each part respectively.
The backend contains embeddings.py, which controls vector embeddings of .md files only, rag.py for the core rag logic and main.py for API endpoints.
The data folder contains folders for professional, academic and personal documents to further keep track of different types of documents.

The frontend folder contains everything for the React application.
```
.
├── backend/
│   ├── embeddings.py   # Handles embedding + saving documents into ChromaDB
│   ├── rag.py          # RAG logic – retrieves relevant context & generates responses
│   ├── main.py         # FastAPI app (query + upload endpoints)
│   └── data/           # Local storage for uploaded documents
│       ├── professional/
│       ├── academic/
│       └── personal/
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx     # React frontend (chat UI + upload sidebar)
│   │   ├── App.css     # Styling for chat + sidebar
│   │   └── index.css   # Base styles / reset
│   ├── package.json    # Frontend dependencies
│   └── public/
│       └── logo.png    # Logo (used in header + favicon)
│
└── README.md           # You are here

```

## ⚙️ Requirements
Backend
- Python 3.10+
- FastAPI
- Uvicorn
- ChromaDB
- LangChain
- Google Generative AI SDK

Frontend
- Node.js 18+
- npm

You also need:
- A Google Gemini API key


## ✨ Tech Stack & Design Choices
- **FastAPI:** Lightweight, async Python backend. Chosen for simplicity and strong ecosystem.
- **ChromaDB:** Local vector store for embeddings. Keeps project self-contained.
- **Google Gemini embeddings:** Converts my documents into dense vector space for semantic retrieval.
- **React:** Flexible, component-based frontend with file upload + chat interface.
- Deployment:
  - **Backend:** Render → simple + free tier + environment variable support.
  - **Frontend:** Vercel → smooth React hosting, preview deployments for testing.

## 💬 Sample quesions and expected answers
Please note that answers vary with each question and might not be the same as the provided expected answers, and that uploading additional files will cause differences in answers. For example, the agent might answer very specifically, even mentioning the company's name to who i applied to, when using information from a cover letter that I uploaded. On the other hand, the agent can also reply very broadly.

- **Question:** "What type of engineer are you?"
  - Expected answer: "I'm not formally titled as any specific kind of engineer. I wouldn't call myself a software engineer, exactly, though I do a lot of coding. Maybe more of a data scientist, or something similar. It's still early in my career, so I haven't really settled on a specific label yet."


- **Question:** "What are your strongest technical skills?"
  - Expected answer: "I'd say my strongest skills are in Python, SQL, and R. I've been working with them for a while now and feel pretty comfortable with the fundamentals and best practices, especially object-oriented programming."
 
- **Question:** "What projects or experiences are you most proud of?"
  - Expected answer: "I'm particularly proud of Project Halyard. Building that AI agent from the ground up, fine-tuning the Qwen-3 model and then identifying areas for improvement during validation testing was a significant challenge. It’s a project that really pushes against existing biases, and that's something I feel strongly about. I also enjoyed working on BioGraph; creating the ETL pipeline to unify those biological databases into a graph database was a complex but rewarding problem. The interactive GUI I built using PyQt6 was also a highlight of that project."

Answers may vary but are more or less along the lines of the expected answers. Feel free to ask it anything about my career/education/projects


## 🛠 Future improvements
With more time and perhaps in the future, I would like to add these improvements to the project:
- Fine-tuning the LLM
  - The LLM struggles to speak in my tone, so finetuning the model on my writing style could hopefully add more realism to the agent.
- Deletion of files in the database
  - So far, a user is only able to add files to the database. If the files are incorrect, there is no way of deleting them.
- Fix context problems
  - When testing out the agent in development, I noticed that whenever I added a very large file, most of the answers by the LLM would come from using ONLY chunks from that file as context, even if the answers aren't anywhere in that file. I believe that it is caused by too many chunks from that one document, while very little from others. I think it is from the relatively small files (+- 1 page), making very little chunks for each document.

## 🧠 Show your thinking artifacts

### Prompt history
The below gives some insights into the prompts that were given to LLM's such as ChatGPT and Gemini:
- "This is the jsx file for a react project that i am working on. it uses tailwind css, but i do not want to use tailwind anymore. i want to do traditional styling with normal css. change my app.jsx to reflect this and provide the code for App.jsx and index.html."
- "please help me brainstorm the architecture (of the project), as well as which files I could include that would show my professional, academic and personal side (separately)."
- "what prompt template can i provide so that the response from the agent is in first person (it should reply like it is me), and it feels like a response a human would give and not a LLM"
- "PermissionError: [WinError 5] Access is denied: 'chroma'. i get this error when i run the code"
- "create a file called rag.py which is the core of the rag agent. it allows for querying and where i set up the agent context"

### Tying code blocks back to AI prompts
These are just some prompts and how they helped build the project. There are of course many more but these are just two examples to show how the code AI produced was used to help with the final code but build the final code completely.
- Prompt: how do i adjust the width of the chat wrapper so that i can control where the chat box lies
    - AI response:
    - ```
      .chat-wrapper {
      flex: none;
      width: 1000px;   /* control this width */
      display: flex;
      justify-content: center;
      }
      ```
  - Final code block:
  - ```
    .chat-wrapper {
    flex: 1; /* take remaining space */
    /*width: 1200px;*/
    display: flex;
    justify-content: center; /* center horizontally */
    align-items: center;     /* center vertically if wanted */
    }
    ```
- Prompt: what do you think is a good chunk size and chunk overlap for my files given their size?
  - AI response:
  - ```
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150,
    separators=["\n\n", "\n", " ", ""]
    )
    ```
  - Final code block:
  - ```
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, # chosen for the relatively small size of the documents
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    ```
- Prompt: Provide the code for main.py to expose my API endpoints using FastAPI
  - AI response:
  - ```
    @app.get("/ask")
    def ask(query: str):
      return {"answer": generate_answer(query)}
    ```
  - Final code block:
  - ```
    @app.post("/query", response_model=RAGResponse)
    async def query_agent(request: QueryRequest):

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
    ```

### Commits generated by AI
While Python is one of my most proficient programming languages, I still had trouble implementing ChromaDB and it was my first time using FastAPI. Significant parts of the backend were produced by AI, but majority of the code was edited by me, as it was either buggy or not what I intended. 

All of my frontend except certain css code (such as colours, borders, font sizes) was produced by AI. I have little to no experience in frontend development and greatly needed AI's assistance with this stage of the project.

AI also provided me with step by step guides on how to deploy my project, as I had no prior experience with Vercel and Render.
