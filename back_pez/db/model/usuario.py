from typing import List

from back_pez.db.model.perfilEstudiante import PerfilEstudiante
from back_pez.db.model.programa import Programa

from sqlalchemy.orm import mapped_column
from .base import Base
from sqlalchemy.orm import Mapped

from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey

usuarios_programas = Table(
    "usuarios_programas",
    Base.metadata,
    Column("usuarios_id", ForeignKey("usuarios.id"), primary_key=True),
    Column("programas_id", ForeignKey("programas.id"), primary_key=True),
)

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    correo: Mapped[str]
    contrasenia: Mapped[str]
    programa: Mapped[List[Programa]] = relationship(secondary = usuarios_programas)
    tipo: Mapped[str]
    perfilEstudiante: Mapped[PerfilEstudiante]