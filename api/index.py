import sys
import os

# Add the backend directory to sys.path so we can import from 'app'
backend_path = os.path.join(os.path.dirname(__file__), "..", "web-app", "backend")
sys.path.append(backend_path)

from main import app

# This is the entry point for Vercel
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
