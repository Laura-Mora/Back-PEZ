from typing import List

from back_pez.db.model.perfilEstudiante import PerfilEstudiante, PerfilEstudianteModelo
#from back_pez.db.model.programa import Programa

from sqlalchemy.orm import mapped_column

from back_pez.db.model.programa import Programa, ProgramaModel
from .base import Base
from sqlalchemy.orm import Mapped

from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey

from pydantic import BaseModel

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
    perfilEstudiante_id: Mapped[int] = mapped_column(ForeignKey("perfilesEstudiantes.id"))
    perfilEstudiante: Mapped[PerfilEstudiante] = relationship()

class UsuarioModelo(BaseModel):
    __tablename__ = "usuarios"

    id: int
    nombre: str
    correo: str
    contrasenia: str
    programa: List[ProgramaModel]
    tipo: str
    perfilEstudiante_id: int
    perfilEstudiante: PerfilEstudianteModelo