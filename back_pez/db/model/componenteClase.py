from sqlalchemy.orm import mapped_column
from .base import Base
from sqlalchemy.orm import Mapped

from pydantic import BaseModel

class ComponenteClase(Base):
    __tablename__ = "componentesClases"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]

class ComponenteClaseModelo(BaseModel):
    id: int
    nombre: str
    