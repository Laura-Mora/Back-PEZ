from typing import List
from sqlalchemy.orm import mapped_column
from .base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String

from pydantic import BaseModel

#from back_pez.db.model.asignatura import Asignatura
#from back_pez.db.model.asignatura import asignaturas_actividades


class Actividad(Base):
    __tablename__ = "actividades"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = Column(String, nullable=True)
    #asignaturas: Mapped[List[Asignatura]] = relationship(secondary = asignaturas_actividades)

class ActividadModelo(BaseModel):
    id: int
    nombre: str