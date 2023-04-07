from typing import List
from back_pez.db.model.actividad import Actividad, ActividadModelo
from back_pez.db.model.competencia import Competencia, CompetenciaModel
from back_pez.db.model.componenteClase import ComponenteClase, ComponenteClaseModelo
from back_pez.db.model.contenido import Contenido, ContenidoModelo
from back_pez.db.model.horario import Horario, HorarioModel
from back_pez.db.model.modoEnsenianza import ModoEnsenianza, ModoEnsenianzaModel
from back_pez.db.model.profesor import Profesor, ProfesorModel
from back_pez.db.model.reseniaAsignatura import ReseniaAsignatura, ReseniaAsignaturaModelo

from pydantic import BaseModel

from sqlalchemy.orm import mapped_column
from .base import Base
from sqlalchemy.orm import Mapped

from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey

asignaturas_profesores = Table(
    "asignaturas_profesores",
    Base.metadata,
    Column("asignaturas_id", ForeignKey("asignaturas.id"), primary_key=True),
    Column("profesores_id", ForeignKey("profesores.id"), primary_key=True),
)

asignaturas_horarios = Table(
    "asignaturas_horarios",
    Base.metadata,
    Column("asignaturas_id", ForeignKey("asignaturas.id"), primary_key=True),
    Column("horarios_id", ForeignKey("horarios.id"), primary_key=True),
)

asignaturas_competencia = Table(
    "asignaturas_competencia",
    Base.metadata,
    Column("asignaturas_id", ForeignKey("asignaturas.id"), primary_key=True),
    Column("competencias_id", ForeignKey("competencias.id"), primary_key=True),
)

asignaturas_actividades = Table(
    "asignaturas_actividades",
    Base.metadata,
    Column("asignaturas_id", ForeignKey("asignaturas.id"), primary_key=True),
    Column("actividades_id", ForeignKey("actividades.id"), primary_key=True),
)

asignaturas_contenido = Table(
    "asignaturas_contenido",
    Base.metadata,
    Column("asignaturas_id", ForeignKey("asignaturas.id"), primary_key=True),
    Column("contenidos_id", ForeignKey("contenidos.id"), primary_key=True),
)

class Asignatura(Base):
    __tablename__ = "asignaturas"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    poblacionObjetivo: Mapped[str]
    creditos: Mapped[int]
    complejidad: Mapped[str]
    modalidad: Mapped[ComponenteClase] = relationship()
    profesores: Mapped[List[Profesor]] = relationship(secondary = asignaturas_profesores)
    modoEnsenianza: Mapped[ModoEnsenianza] = relationship()
    horarios: Mapped[List[Horario]] = relationship(secondary = asignaturas_horarios)
    competencias: Mapped[List[Competencia]] = relationship(secondary = asignaturas_competencia)
    actividades: Mapped[List[Actividad]] = relationship(secondary = asignaturas_actividades)
    tematicas: Mapped[List[Contenido]] = relationship(secondary = asignaturas_contenido)
    resenias: Mapped[List[ReseniaAsignatura]] = relationship()

class AsignaturaModelo(BaseModel):

    id: int
    nombre: str
    poblacionObjetivo: str
    creditos: int
    complejidad: str
    modalidad: ComponenteClaseModelo 
    profesores: list[ProfesorModel]
    modoEnsenianza: ModoEnsenianzaModel
    horarios: list[HorarioModel]
    competencias: list[CompetenciaModel]
    actividades: list[ActividadModelo]
    tematicas: list[ContenidoModelo]
    resenias: list[ReseniaAsignaturaModelo]
