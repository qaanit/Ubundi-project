# Development Workflow Guide

## Local Testing

To test your changes locally without deploying to production, run both the backend and frontend servers on your machine.

### 1. Start the Backend

1. Open a terminal.
2. Navigate to the backend directory:
   ```bash
   cd backend
   ```
3. Activate the virtual environment:
   ```bash
   ..\venv\Scripts\Activate
   ```
4. Install requirements (if you added new ones):
   ```bash
   pip install -r requirements.txt
   ```
5. Start the server:
   ```bash
   uvicorn main:app --reload
   ```
   The backend will run at `http://localhost:8000`.

### 2. Start the Frontend

1. Open a **new** terminal.
2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
3. Install dependencies (only needed once or if `package.json` changes):
   ```bash
   npm install
   ```
4. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend will typically run at `http://localhost:5173`.

### 3. Vercel Preview (Pull Requests)

Since you are using Vercel for the frontend:
1. Create a new branch for your changes: `git checkout -b my-feature`.
2. Commit and push your changes: `git push origin my-feature`.
3. Open a Pull Request on GitHub.
4. Vercel will automatically build a **Preview Deployment** and post a link in the PR comments. This allows you to test in an environment identical to production.

## Troubleshooting

### CORS Issues
If you see network errors when connecting to the backend locally, check `backend/main.py`. You likely need to uncomment the local origin:

```python
origins = [
    "http://localhost:5173",  # Ensure this is uncommented for local dev
    "https://qaanitgpt.vercel.app",
]
```
