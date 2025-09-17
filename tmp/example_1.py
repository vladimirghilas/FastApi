import random

from fastapi import FastAPI, HTTPException, status,Request
from pydantic import BaseModel

app = FastAPI()

# Глобальное хранилище цитат
fake_quotes = [
    {
        "id": 1,
        "text": "Программирование — это искусство заставлять компьютер делать то, что вы хотите.",
        "author": {
            "first_name": "Ivan",
            "last_name": "Petrov",
            "birth_year": 1900
            }
    },
    {
        "id": 2,
        "text": "Код — это стихи, написанные на языке логики.",
        "author": {
            "first_name": "Nicolai",
            "last_name": "Alexeev",
            "birth_year": 1910
            }
    },
    {
        "id": 3,
        "text": "Когда вам в голову пришла хорошая идея, действуйте незамедлительно",
        "author": {
            "first_name": "Piotr",
            "last_name": "Sidorov",
            "birth_year": 1920
            }
    }
]
last_quote_id = max(q['id'] for q in fake_quotes)

class Author(BaseModel):
    first_name: str
    last_name: str
    birth_year: int

class BaseQuote(BaseModel):
    text: str
    author: Author

class Quote(BaseQuote):
    id: int

class QuoteCreate(BaseQuote):
    pass

@app.get("/")
def root():
    return {"message": "Добро пожаловать в API цитат!"}

@app.get("/quotes", response_model=list[Quote])
def get_fake_quotes():
    return fake_quotes

@app.get("/quotes/{quote_id}")
def get_quote(quote_id: int):
    for q in fake_quotes:
        if q["id"] == quote_id:
            return q
    raise HTTPException(status_code=404, detail="Цитата не найдена")


@app.post("/quotes", response_model=Quote, status_code=status.HTTP_201_CREATED)  # сериализация
# @app.post("/quotes",status_code=status.HTTP_201_CREATED)  # сериализация
def add_quote(quote:QuoteCreate):  # десериализация
    global last_quote_id
    print(f"quote=", quote)
    last_quote_id += 1
    new_quote = {'id': last_quote_id, 'text': quote.text.strip()}
    fake_quotes.append(new_quote)
    return new_quote

@app.put("/quotes/{quote_id}")
def update_quote(quote_id: int, quote: Quote):
    for q in fake_quotes:
       if q['id'] == quote_id:
           q['text'] = quote.text
           return q
    raise HTTPException(status_code=404, detail='Цитата не найдена')

@app.delete('/quotes/{quote_id}')
def delete_quote(quote_id: int):
    for i, q in enumerate(fake_quotes):
        if q['id'] == quote_id:
            fake_quotes.pop(i)
            return {"message": "Цитата успешно удалена"}
    raise HTTPException(status_code=404, detail='Цитата не найдена')

@app.get('/quotes/random')
def get_random_quotes():
    if not fake_quotes:
        raise HTTPException(status_code=404, detail="No quotes available")
    return random.choice(fake_quotes)
