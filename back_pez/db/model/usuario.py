from typing import List

from back_pez.db.model.perfilEstudiante import PerfilEstudiante, PerfilEstudianteModelo
#from back_pez.db.model.programa import Programa

from sqlalchemy.orm import mapped_column

from back_pez.db.model.programa import Programa, ProgramaModel
from .base import Base
from sqlalchemy.orm import Mapped

from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKeyConstraint, Integer, String
from sqlalchemy import Table
from sqlalchemy import ForeignKey

from pydantic import BaseModel

usuarios_programas = Table(
    "usuarios_programas",
    Base.metadata,
    Column("usuarios_id", ForeignKey('usuarios.id'), primary_key=True),
    Column("programas_id", ForeignKey(Programa.id), primary_key=True),
    ForeignKeyConstraint(['programas_id'], [Programa.id]),
    ForeignKeyConstraint(['usuarios_id'], ['usuarios.id'])
)

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    correo = Column(String)
    contrasenia = Column(String)
    programa = relationship(Programa,secondary = usuarios_programas)
    tipo = Column(String)
    perfilEstudiante_id = mapped_column(Integer,ForeignKey(PerfilEstudiante.id))
    perfilEstudiante = relationship(PerfilEstudiante)

class UsuarioModelo(BaseModel):

    id: int
    nombre: str
    correo: str
    contrasenia: str
    programa: List[ProgramaModel]
    tipo: str
    perfilEstudiante_id: int
    perfilEstudiante: PerfilEstudianteModelo