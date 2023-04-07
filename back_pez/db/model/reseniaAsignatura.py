from typing import List
from sqlalchemy.orm import mapped_column
from .base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from pydantic import BaseModel

#from back_pez.db.model.asignatura import Asignatura

class ReseniaAsignatura(Base):
    __tablename__ = "reseniaAsignatura"

    id: Mapped[int] = mapped_column(primary_key=True)
    aprendizaje: Mapped[bool]
    tematicaRequeridas: Mapped[bool]
    estrategiasPedagogicasProfesor: Mapped[bool]
    actividadesAsignatura: Mapped[bool]
    complejidad: Mapped[str]
    agradoProfesor: Mapped[bool]
    vidaOTrabajo: Mapped[str]
    cargaAsigantura: Mapped[bool]
    nivelExigencia: Mapped[str]
    entregaNotas: Mapped[bool]
    retroalimentacion: Mapped[bool]
    comentarios: Mapped[str]
    incidenciaProfesor: Mapped[str]
   # asignatura: Mapped[Asignatura]

class ReseniaAsignaturaModelo(BaseModel):

    id: int
    aprendizaje: bool
    tematicaRequeridas: bool
    estrategiasPedagogicasProfesor: bool
    actividadesAsignatura: bool
    complejidad: str
    agradoProfesor: bool
    vidaOTrabajo: str
    cargaAsigantura: bool
    nivelExigencia: str
    entregaNotas: bool
    retroalimentacion: bool
    comentarios: str
    incidenciaProfesor: str