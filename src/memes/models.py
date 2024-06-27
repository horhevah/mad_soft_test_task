import datetime

from src.database import Base
from sqlalchemy import Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column


class Memes(Base):
    __tablename__ = 'memes'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str]
    category: Mapped[str]
    image: Mapped[str]
    created_at: Mapped[datetime.datetime]
