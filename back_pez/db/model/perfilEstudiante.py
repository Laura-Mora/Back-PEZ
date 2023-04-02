from typing import List

from back_pez.db.model.actividad import Actividad
from back_pez.db.model.asignatura import Asignatura
from back_pez.db.model.competencia import Competencia
from back_pez.db.model.componenteClase import ComponenteClase
from back_pez.db.model.contenido import Contenido
from back_pez.db.model.horario import Horario
from back_pez.db.model.modoEnsenianza import ModoEnsenianza

from sqlalchemy.orm import mapped_column
from .base import Base
from sqlalchemy.orm import Mapped

from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey

perfiles_asignaturasCursadas = Table(
    "perfiles_asignaturasCursadas",
    Base.metadata,
    Column("perfilesEstudiantes_id", ForeignKey("perfilesEstudiantes.id"), primary_key=True),
    Column("asignaturas_id", ForeignKey("asignaturas.id"), primary_key=True),
)

perfiles_asignaturasGustadas = Table(
    "perfiles_asignaturasGustadas",
    Base.metadata,
    Column("perfilesEstudiantes_id", ForeignKey("perfilesEstudiantes.id"), primary_key=True),
    Column("asignaturas_id", ForeignKey("asignaturas.id"), primary_key=True),
)

perfiles_modalidades = Table(
    "perfiles_modalidades",
    Base.metadata,
    Column("perfilesEstudiantes_id", ForeignKey("perfilesEstudiantes.id"), primary_key=True),
    Column("componentesClases_id", ForeignKey("componentesClases.id"), primary_key=True),
)

perfiles_modosEnsenianza = Table(
    "perfiles_modosEnsenianza",
    Base.metadata,
    Column("perfilesEstudiantes_id", ForeignKey("perfilesEstudiantes.id"), primary_key=True),
    Column("modosEnsenianza_id", ForeignKey("modosEnsenianza.id"), primary_key=True),
)

perfiles_horarios = Table(
    "perfiles_horarios",
    Base.metadata,
    Column("perfilesEstudiantes_id", ForeignKey("perfilesEstudiantes.id"), primary_key=True),
    Column("horarios_id", ForeignKey("horarios.id"), primary_key=True),
)

perfiles_competencias = Table(
    "perfiles_competencias",
    Base.metadata,
    Column("perfilesEstudiantes_id", ForeignKey("perfilesEstudiantes.id"), primary_key=True),
    Column("competencias_id", ForeignKey("competencias.id"), primary_key=True),
)

perfiles_actividades = Table(
    "perfiles_actividades",
    Base.metadata,
    Column("perfilesEstudiantes_id", ForeignKey("perfilesEstudiantes.id"), primary_key=True),
    Column("actividades_id", ForeignKey("actividades.id"), primary_key=True),
)

perfiles_contenidos = Table(
    "perfiles_contenidos",
    Base.metadata,
    Column("perfilesEstudiantes_id", ForeignKey("perfilesEstudiantes.id"), primary_key=True),
    Column("contenidos_id", ForeignKey("contenidos.id"), primary_key=True),
)

class PerfilEstudiante(Base):
    __tablename__ = "perfilesEstudiantes"

    id: Mapped[int] = mapped_column(primary_key=True)
    profesion: Mapped[str]
    javeriano: Mapped[bool]
    semestre: Mapped[int]
    areaDesempenio: Mapped[str]
    asignaturasCursadas: Mapped[List[Asignatura]] = relationship(secondary = perfiles_asignaturasCursadas)
    asignaturasGustadas: Mapped[List[Asignatura]] = relationship(secondary = perfiles_asignaturasGustadas)
    modalidadPreferencia: Mapped[List[ComponenteClase]] = relationship(secondary = perfiles_modalidades)
    modoEnsenianzaPreferencia: Mapped[List[ModoEnsenianza]] = relationship(secondary = perfiles_modosEnsenianza)
    horariosPreferencias: Mapped[List[Horario]] = relationship(secondary = perfiles_horarios)
    competenciasGusto: Mapped[List[Competencia]] = relationship(secondary = perfiles_competencias)
    actividadesGusto: Mapped[List[Actividad]] = relationship(secondary = perfiles_actividades)
    tematicasGusto: Mapped[List[Contenido]] = relationship(secondary = perfiles_contenidos)