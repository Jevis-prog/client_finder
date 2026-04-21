from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.api import api_router
from config import FASTAPI_ALLOW_ORIGINS


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=FASTAPI_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'OPTIONS'],
    allow_headers=['Content-Type'],
)

app.include_router(api_router, prefix='/api/v1', tags=['v1'])
