import uuid  # id = str(uuid.uuid4())
from fastapi import HTTPException, status

# Имитация хранилища данных с использованием словарей в памяти.
quotes_db: dict[int, dict] = {
    1: {"id": 1,
        "text": "Программирование — это искусство заставлять ...",
        "author_id": 1
        },
    2: {
        "id": 2,
        "text": "Код — это стихи, написанные на языке логики.",
        "author_id": 1
    }
}

authors_db: dict[int, dict] = {
    1: {
        "id": 1,
        "first_name": "Piotr",
        "last_name": "Sidorov",
        "birth_year": 1920
        }
}

last_quote_id = max(quotes_db.keys(), default=0)
last_author_id = max(authors_db.keys(), default=0)
# Функции для работы с цитатами
def create_quote(quote: dict) -> dict | None:
    """Создает новую цитату."""
    global last_quote_id

    author = get_author_by_id(quote['author_id'])
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id={quote['author_id']} not found"
        )
    new_quote = {
        'id': last_quote_id+1,
        'text': quote['text'],
        'author_id': quote['author_id'],
        'author': author
    }
    quotes_db[last_quote_id+1] = new_quote
    last_quote_id += 1
    return new_quote

def get_quote_by_id(quote_id: int) -> dict | None:
    """Получает цитату по ID."""
    return quotes_db.get(quote_id)

def get_all_quotes() -> list[dict]:
    """Возвращает список всех цитат."""
    quotes = list(quotes_db.values())
    for quote in quotes:
        author = get_author_by_id(quote['author_id'])
        quote['author'] = author
    return quotes

def get_quotes_by_author(author_id: int) -> list[dict]:
    """Возвращает все цитаты указанного автора."""
    return [{**quote,  "author": get_author_by_id(author_id)}
            for quote in quotes_db.values()
            if quote["author_id"] == author_id
            ]

def update_quote(quote_id: int, new_data: dict) -> dict | list:
    """Обновляет данные цитаты."""
    quote = quotes_db.get(quote_id)
    if not quote:
        return {"error": "Цитата не найдена"}

    quote.update(new_data)
    return quote

def delete_quote(quote_id: int) -> bool:
    """Удаляет цитату."""

    if quote_id in quotes_db:
        del quotes_db[quote_id]
        return True
    return False

# Функции для работы с авторами
def create_author(author: dict) -> dict:
    """Создает нового автора."""
    global last_author_id
    last_author_id +=1
    new_author = {"id": last_author_id, **author}
    authors_db[last_author_id] = new_author
    return new_author

def get_author_by_id(author_id: int) -> dict | None:
    """Получает автора по ID."""
    return authors_db.get(author_id)

def get_all_authors() -> list[dict]:
    """Возвращает список всех авторов."""
    return list(authors_db.values())

def update_author(author_id: int, new_data: dict) -> dict | None:
    """Обновляет данные автора."""
    author = authors_db.get(author_id)
    if not author:
        return {"error": "Автор не найден"}
    author.update(new_data)
    return author

def delete_author(author_id: int) -> bool:
    """Удаляет автора и связанные с ним цитаты."""
    if author_id in authors_db:
        del authors_db[author_id]
        # Удаляем автора и все цитаты этого автора
        to_delete = [qid for qid, q in quotes_db.items() if q["author_id"] == author_id]
        for qid in to_delete:
            del quotes_db[qid]
        return True
    return False
