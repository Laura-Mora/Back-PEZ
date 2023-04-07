from back_pez.db.model.componente import Componente, ComponenteModelo
from sqlalchemy.orm import mapped_column

from back_pez.db.model.usuario import Usuario
from back_pez.db.model.usuario import usuarios_programas
from .base import Base

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey

from typing import List

from pydantic import BaseModel

programas_componentes= Table(
    "programas_componentes",
    Base.metadata,
    Column("programas_id", ForeignKey("programas.id"), primary_key=True),
    Column("componentes_id", ForeignKey("componentes.id"), primary_key=True),
)

class Programa(Base):
    __tablename__ = "programas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    cantCreditos: Mapped[int]
    componentes: Mapped[List[Componente]] = relationship(secondary = programas_componentes)
    #usuarios: Mapped[List[Usuario]] = relationship(secondary = usuarios_programas)
    
class ProgramaModel(BaseModel):

    id: int
    nombre:str
    cantCreditos: int
    componentes: List[ComponenteModelo]