from typing import List
from sqlalchemy.orm import mapped_column
from .base import Base
from sqlalchemy.orm import Mapped

from back_pez.db.model.asignatura import Asignatura
from back_pez.db.model.subComponente import subComponente

from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey

componentes_asignaturasObli = Table(
    "componentes_asignaturasObli",
    Base.metadata,
    Column("componentes_id", ForeignKey("componentes.id"), primary_key=True),
    Column("asignaturas_id", ForeignKey("asignaturas.id"), primary_key=True),
)

componentes_asignaturasElec = Table(
    "componentes_asignaturasObli",
    Base.metadata,
    Column("componentes_id", ForeignKey("componentes.id"), primary_key=True),
    Column("asignaturas_id", ForeignKey("asignaturas.id"), primary_key=True),
)

class Componente(Base):
    __tablename__ = "Componentes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    cantCreditos: Mapped[int]
    asignaturasObligatorias: Mapped[List[Asignatura]] = relationship(secondary = componentes_asignaturasObli)
    asignaturasElectivas: Mapped[List[Asignatura]] = relationship(secondary = componentes_asignaturasElec)
    subcomponentes: Mapped[List[subComponente]] = relationship()