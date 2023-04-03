from typing import List
from sqlalchemy.orm import mapped_column
from .base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from back_pez.db.model.asignatura import Asignatura
from back_pez.db.model.asignatura import asignaturas_profesores



class Profesor(Base):
    __tablename__ = "profesores"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    asignaturas: Mapped[List[Asignatura]] = relationship(secondary = asignaturas_profesores)
    

