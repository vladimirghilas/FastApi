from database import SessionLocal
from models.authors import Author
from models.quotes import Quote
from sqlalchemy import select

print("from database import SessionLocal")
print("from models.authors import Author")
print("from models.quotes import Quote")
print("from sqlalchemy import select")

session = SessionLocal()