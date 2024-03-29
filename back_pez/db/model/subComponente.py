from typing import List
from sqlalchemy.orm import mapped_column
from .base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKeyConstraint
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer

from pydantic import BaseModel

from db.model.asignatura import Asignatura, AsignaturaModelo

subcomponentes_asignaturasObli = Table(
    "subcomponentes_asignaturasObli",
    Base.metadata,
    Column("subComponentes_id", ForeignKey('subComponentes.id'), primary_key=True),
    Column("asignatura_id", ForeignKey(Asignatura.id), primary_key=True),
    ForeignKeyConstraint(['asignatura_id'], [Asignatura.id]),
    ForeignKeyConstraint(['subComponentes_id'], ['subComponentes.id'])
)

subcomponentes_asignaturasElec = Table(
    "subcomponentes_asignaturasElec",
    Base.metadata,
    Column("subComponentes_id", ForeignKey('subComponentes.id'), primary_key=True),
    Column("asignatura_id", ForeignKey(Asignatura.id), primary_key=True),
    ForeignKeyConstraint(['asignatura_id'], [Asignatura.id]),
    ForeignKeyConstraint(['subComponentes_id'], ['subComponentes.id'])
)

class subComponente(Base):
    __tablename__ = 'subComponentes'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    nombre: Mapped[str]
    cantCreditos: Mapped[int] = Column(Integer, nullable=True)
    cantAsignaturas: Mapped[int] = Column(Integer, nullable=True)
    asignaturasObligatorias = relationship(Asignatura, secondary=subcomponentes_asignaturasObli)
    asignaturasElectivas = relationship(Asignatura, secondary=subcomponentes_asignaturasElec)

class subComponenteModelo(BaseModel):

    id: int
    nombre: str
    cantCreditos: int = None
    cantAsignaturas: int = None
    asignaturasObligatorias: List[AsignaturaModelo] = None
    asignaturasElectivas:List[AsignaturaModelo] = None
    