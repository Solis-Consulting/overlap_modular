from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware
import os
import sys

# Ensure the repo root (where overlapv4.py and JSONs live) is importable
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Import the Dash app defined in overlapv4.py (exports app = dash.Dash(...))
import overlapv4  # uses overlapv4.app.server

# ASGI app for Vercel
app = FastAPI()

@app.get("/healthz")
def healthz():
    return {"ok": True}

# Mount Dash (Flask WSGI) at root
app.mount("/", WSGIMiddleware(overlapv4.app.server))
