from typing import List
import datetime
from sqlalchemy.orm import mapped_column
from .base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from pydantic import BaseModel

#from back_pez.db.model.asignatura import Asignatura
#from back_pez.db.model.asignatura import asignaturas_horarios

class Horario(Base):
    __tablename__ = "horarios"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    horaInicio: Mapped[datetime.time]
    horaFinal: Mapped[datetime.time]
    dia: Mapped[str]
    #asignaturas: Mapped[List[Asignatura]] = relationship(secondary = asignaturas_horarios)

class HorarioModel(BaseModel):
    id: int
    dia: str
    horaInicio: datetime.time
    horaFinal: datetime.time


    