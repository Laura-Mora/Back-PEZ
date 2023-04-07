from typing import List
from sqlalchemy.orm import mapped_column
from .base import Base
from sqlalchemy.orm import Mapped

from pydantic import BaseModel

from back_pez.db.model.asignatura import Asignatura, AsignaturaModelo
from back_pez.db.model.subComponente import subComponente, subComponenteModelo

from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey

componentes_asignaturasObli = Table(
    "componentes_asignaturasObli",
    Base.metadata,
    Column("componentes_id", ForeignKey("componentes.id"), primary_key=True),
    Column("asignaturas_id", ForeignKey("asignaturas.id"), primary_key=True),
)

componentes_asignaturasElec = Table(
    "componentes_asignaturasElec",
    Base.metadata,
    Column("componentes_id", ForeignKey("componentes.id"), primary_key=True),
    Column("asignaturas_id", ForeignKey("asignaturas.id"), primary_key=True),
)

class Componente(Base):
    __tablename__ = "Componentes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    cantCreditos: Mapped[int]

class ComponenteObligactoria(Base):
    __tablename__ = "ComponentesObligactorias"
    
    asignaturasObligatorias: Mapped[List[Asignatura]] = relationship(secondary = componentes_asignaturasObli)
    componente_id: Mapped[int] = mapped_column(ForeignKey("Componentes.id"),primary_key=True)
    componente: Mapped[Componente] = relationship(back_populates="ComponenteObligactoria")
    

class ComponenteElectiva(Base):
    __tablename__ = "ComponentesElectivas"

    asignaturasElectivas: Mapped[List[Asignatura]] = relationship(secondary = componentes_asignaturasElec)
    componente_id: Mapped[int] = mapped_column(ForeignKey("Componentes.id"),primary_key=True)
    componente: Mapped[Componente] = relationship(back_populates="ComponentesElectiva")

class ComponenteSubComponente(Base):
    __tablename__ = "ComponentesSubComponente"

    subcomponentes: Mapped[List[subComponente]] = relationship()
    componente_id: Mapped[int] = mapped_column(ForeignKey("Componentes.id"),primary_key=True)
    componente: Mapped[Componente] = relationship(back_populates="ComponentesSubComponente")

class ComponenteModelo(BaseModel):
    id: int
    nombre: str
    cantCreditos: int
    asignaturasObligatorias: List[AsignaturaModelo]
    asignaturasElectivas: List[AsignaturaModelo]
    subcomponentes: List[subComponenteModelo]
