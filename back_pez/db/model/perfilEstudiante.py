from typing import List

from back_pez.db.model.actividad import Actividad, ActividadModelo
from back_pez.db.model.asignatura import Asignatura, AsignaturaModelo
from back_pez.db.model.competencia import Competencia, CompetenciaModel
from back_pez.db.model.componenteClase import ComponenteClase, ComponenteClaseModelo
from back_pez.db.model.contenido import Contenido, ContenidoModelo
from back_pez.db.model.horario import Horario, HorarioModel
from back_pez.db.model.modoEnsenianza import ModoEnsenianza, ModoEnsenianzaModel

from sqlalchemy.orm import mapped_column
from .base import Base
from sqlalchemy.orm import Mapped

from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, ForeignKeyConstraint, Integer, String
from sqlalchemy import Table
from sqlalchemy import ForeignKey

from pydantic import BaseModel

perfiles_asignaturasCursadas = Table(
    'perfiles_asignaturasCursadas',
    Base.metadata,
    Column("perfilesEstudiantes_id", ForeignKey('perfilesEstudiantes.id'), primary_key=True),
    Column("asignatura_id", ForeignKey(Asignatura.id), primary_key=True),
    ForeignKeyConstraint(['asignatura_id'], [Asignatura.id]),
    ForeignKeyConstraint(['perfilesEstudiantes_id'], ['perfilesEstudiantes.id'])
)

perfiles_asignaturasGustadas = Table(
    'perfiles_asignaturasGustadas',
    Base.metadata,
    Column("perfilesEstudiantes_id", ForeignKey('perfilesEstudiantes.id'), primary_key=True),
    Column("asignatura_id", ForeignKey(Asignatura.id), primary_key=True),
    ForeignKeyConstraint(['asignatura_id'], [Asignatura.id]),
    ForeignKeyConstraint(['perfilesEstudiantes_id'], ['perfilesEstudiantes.id'])
)

perfiles_modalidades = Table(
    "perfiles_modalidades",
    Base.metadata,
    Column("perfilesEstudiantes_id", ForeignKey('perfilesEstudiantes.id'), primary_key=True),
    Column("componentesClases_id", ForeignKey(ComponenteClase.id), primary_key=True),
    ForeignKeyConstraint(['componentesClases_id'], [ComponenteClase.id]),
    ForeignKeyConstraint(['perfilesEstudiantes_id'], ['perfilesEstudiantes.id'])
)

perfiles_modosEnsenianza = Table(
    "perfiles_modosEnsenianza",
    Base.metadata,
    Column("perfilesEstudiantes_id", ForeignKey("perfilesEstudiantes.id"), primary_key=True),
    Column("modosEnsenianza_id", ForeignKey(ModoEnsenianza.id), primary_key=True),
    ForeignKeyConstraint(['modosEnsenianza_id'], [ModoEnsenianza.id]),
    ForeignKeyConstraint(['perfilesEstudiantes_id'], ['perfilesEstudiantes.id'])
)

perfiles_horarios = Table(
    "perfiles_horarios",
    Base.metadata,
    Column("perfilesEstudiantes_id", ForeignKey("perfilesEstudiantes.id"), primary_key=True),
    Column("horarios_id", ForeignKey(Horario.id), primary_key=True),
    ForeignKeyConstraint(['horarios_id'], [Horario.id]),
    ForeignKeyConstraint(['perfilesEstudiantes_id'], ['perfilesEstudiantes.id'])
)

perfiles_competencias = Table(
    "perfiles_competencias",
    Base.metadata,
    Column("perfilesEstudiantes_id", ForeignKey("perfilesEstudiantes.id"), primary_key=True),
    Column("competencias_id", ForeignKey(Competencia.id), primary_key=True),
    ForeignKeyConstraint(['competencias_id'], [Competencia.id]),
    ForeignKeyConstraint(['perfilesEstudiantes_id'], ['perfilesEstudiantes.id'])
)

perfiles_actividades = Table(
    "perfiles_actividades",
    Base.metadata,
    Column("perfilesEstudiantes_id", ForeignKey("perfilesEstudiantes.id"), primary_key=True),
    Column("actividades_id", ForeignKey(Actividad.id), primary_key=True),
    ForeignKeyConstraint(['actividades_id'], [Actividad.id]),
    ForeignKeyConstraint(['perfilesEstudiantes_id'], ['perfilesEstudiantes.id'])
)

perfiles_contenidos = Table(
    "perfiles_contenidos",
    Base.metadata,
    Column("perfilesEstudiantes_id", ForeignKey("perfilesEstudiantes.id"), primary_key=True),
    Column("contenidos_id", ForeignKey(Contenido.id), primary_key=True),
    ForeignKeyConstraint(['contenidos_id'], [Contenido.id]),
    ForeignKeyConstraint(['perfilesEstudiantes_id'], ['perfilesEstudiantes.id'])
)

class PerfilEstudiante(Base):
    __tablename__ = 'perfilesEstudiantes'

    id = Column(Integer, primary_key=True)
    profesion = Column(String)
    javeriano = Column(Boolean)
    semestre = Column(Integer)
    areaDesempenio = Column(String)
    asignaturasCursadas = relationship(Asignatura, secondary = perfiles_asignaturasCursadas)
    asignaturasGustadas = relationship(Asignatura, secondary = perfiles_asignaturasGustadas)
    modalidadPreferencia = relationship(ComponenteClase,secondary = perfiles_modalidades)
    modoEnsenianzaPreferencia = relationship(ModoEnsenianza,secondary = perfiles_modosEnsenianza)
    horariosPreferencias = relationship(Horario,secondary = perfiles_horarios)
    competenciasGusto = relationship(Competencia,secondary = perfiles_competencias)
    actividadesGusto = relationship(Actividad, secondary = perfiles_actividades)
    tematicasGusto = relationship(Contenido,secondary = perfiles_contenidos)

class PerfilEstudianteModelo(BaseModel):
 
    id: int
    profesion: str
    javeriano: bool
    semestre: int
    areaDesempenio: str
    asignaturasCursadas: List[AsignaturaModelo]
    asignaturasGustadas: List[AsignaturaModelo]
    modalidadPreferencia: List[ComponenteClaseModelo]
    modoEnsenianzaPreferencia: List[ModoEnsenianzaModel]
    horariosPreferencias: List[HorarioModel]
    competenciasGusto: List[CompetenciaModel]
    actividadesGusto: List[ActividadModelo]
    tematicasGusto: List[ContenidoModelo]