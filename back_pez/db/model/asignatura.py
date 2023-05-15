from typing import List
from back_pez.db.model.actividad import Actividad, ActividadModelo
from back_pez.db.model.competencia import Competencia, CompetenciaModel
from back_pez.db.model.componenteClase import ComponenteClase, ComponenteClaseModelo
from back_pez.db.model.tematica import Tematica, TematicaModelo
from back_pez.db.model.horario import Horario, HorarioModel
from back_pez.db.model.modoEnsenianza import ModoEnsenianza, ModoEnsenianzaModel
from back_pez.db.model.profesor import Profesor, ProfesorModel

from pydantic import BaseModel

from sqlalchemy.orm import mapped_column
from .base import Base
from sqlalchemy.orm import Mapped

from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKeyConstraint, Integer, String
from sqlalchemy import Table
from sqlalchemy import ForeignKey

asignaturas_profesores = Table(
    "asignaturas_profesores",
    Base.metadata,
    Column("asignaturas_id", ForeignKey('asignaturas.id'), primary_key=True),
    Column("profesores_id", ForeignKey(Profesor.id), primary_key=True),
    ForeignKeyConstraint(['profesores_id'], [Profesor.id]),
    ForeignKeyConstraint(['asignaturas_id'], ['asignaturas.id'])
)

asignaturas_horarios = Table(
    "asignaturas_horarios",
    Base.metadata,
    Column("asignaturas_id", ForeignKey("asignaturas.id"), primary_key=True),
    Column("horarios_id", ForeignKey(Horario.id), primary_key=True),
    ForeignKeyConstraint(['horarios_id'], [Horario.id]),
    ForeignKeyConstraint(['asignaturas_id'], ['asignaturas.id'])
)

asignaturas_competencia = Table(
    "asignaturas_competencia",
    Base.metadata,
    Column("asignaturas_id", ForeignKey("asignaturas.id"), primary_key=True),
    Column("competencias_id", ForeignKey(Competencia.id), primary_key=True),
    ForeignKeyConstraint(['competencias_id'], [Competencia.id]),
    ForeignKeyConstraint(['asignaturas_id'], ['asignaturas.id'])
)

asignaturas_actividades = Table(
    "asignaturas_actividades",
    Base.metadata,
    Column("asignaturas_id", ForeignKey("asignaturas.id"), primary_key=True),
    Column("actividades_id", ForeignKey(Actividad.id), primary_key=True),
    ForeignKeyConstraint(['actividades_id'], [Actividad.id]),
    ForeignKeyConstraint(['asignaturas_id'], ['asignaturas.id'])
)


asignaturas_tematica = Table(
    "asignaturas_tematica",
    Base.metadata,
    Column("asignaturas_id", ForeignKey("asignaturas.id"), primary_key=True),
    Column("tematica_id", ForeignKey(Tematica.id), primary_key=True),
    ForeignKeyConstraint(['tematica_id'], [Tematica.id]),
    ForeignKeyConstraint(['asignaturas_id'], ['asignaturas.id'])
)

class Asignatura(Base):
    __tablename__ = 'asignaturas'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    poblacionObjetivo = Column(String)
    creditos = Column(Integer)
    complejidad = Column(String)
    componenteClase_id = Column(Integer, ForeignKey(ComponenteClase.id))
    modalidad = relationship(ComponenteClase)
    profesores = relationship(Profesor, secondary=asignaturas_profesores)
    modoEnsenianza_id = Column(Integer, ForeignKey(ModoEnsenianza.id))
    modoEnsenianza = relationship(ModoEnsenianza)
    horarios = relationship(Horario, secondary=asignaturas_horarios)
    competencias = relationship(Competencia, secondary=asignaturas_competencia)
    actividades = relationship(Actividad, secondary=asignaturas_actividades)
    tematicas = relationship(Tematica, secondary=asignaturas_tematica)


class AsignaturaModelo(BaseModel):

    id: int
    nombre: str
    poblacionObjetivo: str = None
    creditos: int = None
    complejidad: str = None
    modalidad: ComponenteClaseModelo = None
    profesores: list[ProfesorModel] = None
    modoEnsenianza: ModoEnsenianzaModel = None
    horarios: list[HorarioModel] = None
    competencias: list[CompetenciaModel] = None
    actividades: list[ActividadModelo] = None
    tematicas: list[TematicaModelo] = None

