from typing import List
from sqlalchemy.orm import mapped_column
from .base import Base
from sqlalchemy.orm import Mapped

from pydantic import BaseModel

from db.model.asignatura import Asignatura, AsignaturaModelo
from db.model.subComponente import subComponente, subComponenteModelo


from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKeyConstraint, Integer, String
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy import MetaData

metadata = MetaData()


componentes_asignaturasObli = Table(
    "componentes_asignaturasObli",
    Base.metadata,
    Column("componente_id", Integer, ForeignKey('componentes_obligatorios.componente_id'), primary_key=True),
    Column("asignatura_id", Integer, ForeignKey(Asignatura.id), primary_key=True),
    ForeignKeyConstraint(['asignatura_id'], [Asignatura.id]),
    ForeignKeyConstraint(['componente_id'], ['componentes_obligatorios.componente_id'])
)

componentes_asignaturasElec = Table(
    "componentes_asignaturasElec",
    Base.metadata,
    Column("componente_id", ForeignKey('componentes_electivas.componente_id'), primary_key=True),
    Column("asignaturas_id", ForeignKey(Asignatura.id), primary_key=True),
    ForeignKeyConstraint(['asignaturas_id'], [Asignatura.id]),
    ForeignKeyConstraint(['componente_id'], ['componentes_electivas.componente_id'])
)

componente_subComponentes = Table(
    "componente_subComponentes",
    Base.metadata,
    Column("componente_id", ForeignKey('ComponentesSubComponente.componente_id'), primary_key=True),
    Column("subComponente_id", ForeignKey(subComponente.id), primary_key = True),
    ForeignKeyConstraint(['subComponente_id'],[subComponente.id]),
    ForeignKeyConstraint(['componente_id'], ['ComponentesSubComponente.componente_id'])
)

class Componente(Base):
    __tablename__ = 'Componentes'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    cantCreditos = Column(Integer)

class ComponenteObligactoria(Base):
    __tablename__ = 'componentes_obligatorios'
    __table_args__ = {'extend_existing': True}

    componente_id = Column(Integer, ForeignKey('Componentes.id'), primary_key=True)
    componente = relationship(Componente)
    asignaturasObligatorias = relationship(Asignatura, secondary=componentes_asignaturasObli)

class ComponenteElectiva(Base):
    __tablename__ = 'componentes_electivas'
    __table_args__ = {'extend_existing': True}

    componente_id = Column(Integer, ForeignKey('Componentes.id'), primary_key=True)
    componente = relationship(Componente)
    asignaturasElectivas = relationship(Asignatura, secondary=componentes_asignaturasElec)

class ComponenteSubComponente(Base):
    __tablename__ = "ComponentesSubComponente"
    __table_args__ = {'extend_existing': True}

    subcomponentes = relationship(subComponente, secondary=componente_subComponentes)
    componente_id: Mapped[int] = mapped_column(ForeignKey('Componentes.id'),primary_key=True)
    componente = relationship(Componente)

class ComponenteModelo(BaseModel):
    id: int
    nombre: str
    cantCreditos: int = None
    asignaturasObligatorias: List[AsignaturaModelo] = None
    asignaturasElectivas: List[AsignaturaModelo] = None
    subcomponentes: List[subComponenteModelo] = None
