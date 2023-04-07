from typing import List
from sqlalchemy.orm import mapped_column
from .base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer

from pydantic import BaseModel

from back_pez.db.model.asignatura import Asignatura, AsignaturaModelo

subcomponentes_asignaturasObli = Table(
    "subcomponentes_asignaturasObli",
    Base.metadata,
    Column("subComponentes_id", ForeignKey("subComponentes.id"), primary_key=True),
    Column("asignaturas_id", ForeignKey("asignaturas.id"), primary_key=True),
)

subcomponentes_asignaturasElec = Table(
    "subcomponentes_asignaturasElec",
    Base.metadata,
    Column("subComponentes_id", ForeignKey("subComponentes.id"), primary_key=True),
    Column("asignaturas_id", ForeignKey("asignaturas.id"), primary_key=True),
)

class subComponente(Base):
    __tablename__ = "subComponentes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    cantCreditos: Mapped[int] = Column(Integer, nullable=True)
    cantAsignaturas: Mapped[int] = Column(Integer, nullable=True)
    asignaturasObligatorias: Mapped[List[Asignatura]] = relationship(secondary = subcomponentes_asignaturasObli)
    asignaturasElectivas: Mapped[List[Asignatura]] = relationship(secondary = subcomponentes_asignaturasElec)

class subComponenteModelo(BaseModel):

    id: int
    nombre: str
    cantCreditos: int
    cantAsignaturas: int
    asignaturasObligatorias: List[AsignaturaModelo]
    asignaturasElectivas:List[AsignaturaModelo]
    