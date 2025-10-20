from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware
import os, sys

# ensure root (where overlapv4.py + JSON files live) is on path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import overlapv4  # defines `app = dash.Dash(...)` with `.server` (Flask) :contentReference[oaicite:0]{index=0}

app = FastAPI()
app.mount("/", WSGIMiddleware(overlapv4.app.server))
