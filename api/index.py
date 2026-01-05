import sys
import os

# Get the root directory
root_path = os.path.dirname(os.path.dirname(__file__))

# Add PyJHora and Backend to path
sys.path.append(os.path.join(root_path, "PyJHora", "src"))
sys.path.append(os.path.join(root_path, "web-app", "backend"))

# Change directory to backend so relative file lookups (like CSVs) work
os.chdir(os.path.join(root_path, "web-app", "backend"))

from fastapi import FastAPI
from mangum import Mangum
from main import app

# This is what Vercel calls
handler = Mangum(app, lifespan="off")
