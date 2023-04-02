from back_pez.db.model.componente import Componente
from sqlalchemy.orm import mapped_column
from .base import Base

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey

from typing import List

programas_contenidos= Table(
    "programas_contenidos",
    Base.metadata,
    Column("programas_id", ForeignKey("programas.id"), primary_key=True),
    Column("contenidos_id", ForeignKey("contenidos.id"), primary_key=True),
)

class Programa(Base):
    __tablename__ = "programas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    cantCreditos: Mapped[int]
    componentes: Mapped[List[Componente]] = relationship(secondary = programas_contenidos)
    
    