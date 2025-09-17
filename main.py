from fastapi import FastAPI
from routers import authors, quotes

app = FastAPI()

app.include_router(
    quotes.router,
    prefix='/quotes',
    tags=['quotes']
)

app.include_router(
authors.router,
prefix='/authors',
tags=['authors']
)