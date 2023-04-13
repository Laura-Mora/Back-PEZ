from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import mapped_column
from .base import Base
from sqlalchemy.orm import Mapped

from pydantic import BaseModel

class ComponenteClase(Base):
    __tablename__ = 'componentesClases'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)

class ComponenteClaseModelo(BaseModel):
    id: int
    nombre: str
    