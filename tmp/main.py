from typing import Union

from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

fake_items = [
    {"id": 2, "name": "Книга", "price":10.5, "is_offer": True},
    {"id": 5, "name": "Ручка", "price":2.0, "is_offer": False},
    {"id": 6, "name": "Рюкзак", "price":18.94, "is_offer": False},
]

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}
#
#
# @app.get("/items/{item_id}")
# def get_item(item_id: int):
#     for item in fake_items:
#         if item['id'] == item_id:
#             return item
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail=f"item id={item_id} not found"
#     )
@app.get("/items")
def get_items(param:str = None, generated_in: str = None):
    return {'param': param, 'generated_in': generated_in}

@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    return item

@app.put("/items/{item_id}")
def update_item(item_id: int, new_item_data: Item):
   ...
   return {'success': True}