from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING
from database import Base

if TYPE_CHECKING:
    from models.quotes import Quote

class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    birth_year: Mapped[int]
    quotes: Mapped[List["Quote"]] = relationship(back_populates="author", cascade="all, delete-orphan")
