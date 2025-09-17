from fastapi import APIRouter, HTTPException,Depends,  status, Response

from models import Quote
from schemas.authors import AuthorSchema, AuthorCreateSchema
from database import get_session
from models.authors import Author
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from schemas.quotes import QuoteSchema

router = APIRouter()

@router.get("/", response_model=list[AuthorSchema])
def  get_all_authors(session: Session=Depends(get_session)):
    """Возвращает список всех авторов."""
    stmt = select(Author)
    authors = session.scalars(stmt).all()
    return authors

@router.get("/{author_id}", response_model=AuthorSchema)
def get_author(author_id: int, session: Session=Depends(get_session)):
    # author = storage.get_author_by_id(author_id)
    stmt = select(Author).where(Author.id == author_id)
    author = session.scalars(stmt).first()
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id={author_id} not found"
        )
    return author

@router.post("/", response_model=AuthorSchema, status_code=status.HTTP_201_CREATED)
def create_author(author: AuthorCreateSchema, session: Session=Depends(get_session)):
    # new_author = storage.create_author(author.model_dump())
    db_author = Author(**author.model_dump())
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author

@router.put("/{author_id}", response_model=AuthorCreateSchema)
def update_author(author_id: int, author: AuthorCreateSchema, session: Session=Depends(get_session)):
    # updated = storage.update_author(author_id, author.model_dump())
    stmt = select(Author).where(Author.id == author_id)
    updated = session.scalars(stmt).first()
    if not updated:
        raise HTTPException(status_code=404, detail=f"Author with id={author_id} not found")

    for field, value in author.model_dump().items():
        setattr(updated, field, value)

        session.commit()
        session.refresh(updated)
    return updated

@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, session: Session=Depends(get_session)):
    # deleted = storage.delete_author(author_id)
    # stmt = select(Author).where(Author.id == author_id)
    # author = session.scalars(stmt).first()
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Автор не найден")

    session.delete(author)
    session.commit()
    return Response(status_code=204)
@router.get("/{author_id}/quotes", response_model=List[QuoteSchema])
def get_author_quotes(author_id: int, session: Session = Depends(get_session)):
    stmt = select(Quote).where(Quote.author_id == author_id)
    quotes = session.scalars(stmt).all()
    if not quotes:
        raise HTTPException(status_code=404, detail="Цитаты автора не найдены")
    return quotes