from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware
import overlapv4

app = FastAPI()
app.mount("/", WSGIMiddleware(overlapv4.app.server))
