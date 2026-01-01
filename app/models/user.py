from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime
from datetime import datetime
from typing import Optional
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    password: Mapped[str] = mapped_column(String)
    
    email: Mapped[Optional[str]] = mapped_column(String(120), unique=True)
    
    def __repr__(self) -> str:
        return f"<User(username={self.username!r})>"