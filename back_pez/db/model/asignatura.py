from typing import List
from back_pez.db.model.actividad import Actividad
from back_pez.db.model.competencia import Competencia
from back_pez.db.model.componenteClase import ComponenteClase
from back_pez.db.model.contenido import Contenido
from back_pez.db.model.horario import Horario
from back_pez.db.model.modoEnsenianza import ModoEnsenianza
from back_pez.db.model.profesor import Profesor

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
    "asignaturas_actividadesa",
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
    modalidad: Mapped[ComponenteClase] #Mirar esto en la documentación relacion uno muchos
    profesores: Mapped[List[Profesor]] = relationship(secondary = asignaturas_profesores)
    modoEnsenianza: Mapped[ModoEnsenianza]
    horarios: Mapped[List[Horario]] = relationship(secondary = asignaturas_horarios)
    competencias: Mapped[List[Competencia]] = relationship(secondary = asignaturas_competencia)
    actividades: Mapped[List[Actividad]] = relationship(secondary = asignaturas_actividades)
    tematicas: Mapped[List[Contenido]] = relationship(secondary = asignaturas_contenido)

