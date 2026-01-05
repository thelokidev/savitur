import sys
import os

# Add the backend directory to sys.path so we can import from 'app'
backend_path = os.path.join(os.path.dirname(__file__), "..", "..", "backend")
sys.path.append(backend_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

# Import the main app
from main import app

# Wrap the FastAPI app with Mangum for serverless
handler = Mangum(app, lifespan="off")
