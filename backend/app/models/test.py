from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class Test(Base):
    __tablename__ = "test"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    def __repr__(self):
        return f"<Test(id={self.id}, name='{self.name}')>"
