from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware
import os, sys

# Ensure repo root (where overlapv4.py + JSONs live) is on sys.path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Import the Dash app; overlapv4.app.server is the Flask WSGI app
import overlapv4

# Export ASGI app for Vercel
app = FastAPI()

@app.get("/healthz")
def healthz():
    return {"ok": True}

# Mount Dash at root
app.mount("/", WSGIMiddleware(overlapv4.app.server))
