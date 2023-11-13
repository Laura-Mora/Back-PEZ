from db.model.componente import Componente, ComponenteModelo
from sqlalchemy.orm import mapped_column


from .base import Base

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKeyConstraint, Integer, String, Boolean
from sqlalchemy import Table
from sqlalchemy import ForeignKey

from typing import List

from pydantic import BaseModel

programas_componentes= Table(
    'programas_componentes',
    Base.metadata,
    Column("programas_id", ForeignKey('programas.id'), primary_key=True),
    Column("componentes_id", ForeignKey(Componente.id), primary_key=True),
    ForeignKeyConstraint(['componentes_id'], [Componente.id]),
    ForeignKeyConstraint(['programas_id'], ['programas.id'])
)

class Programa(Base):
    __tablename__ = 'programas'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    cantCreditos = Column(Integer)
    requisitoIngles = Column(Boolean)
    componentes = relationship(Componente,secondary = programas_componentes)
    
class ProgramaModel(BaseModel):

    id: int
    nombre:str
    cantCreditos: int
    componentes: List[ComponenteModelo]
    requisitoIngles: bool