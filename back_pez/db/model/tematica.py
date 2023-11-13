from typing import List
from sqlalchemy.orm import mapped_column

#from back_pez.db.model.asignatura import Asignatura
#from back_pez.db.model.asignatura import asignaturas_contenido

from .base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from pydantic import BaseModel


class Tematica(Base):
    __tablename__ = "tematicas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    #asignaturas: Mapped[List[Asignatura]] = relationship(secondary = asignaturas_contenido)

    
class TematicaModelo(BaseModel):
    id: int
    nombre: str