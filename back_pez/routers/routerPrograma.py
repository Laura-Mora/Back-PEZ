from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import sessionmaker
from db.model.programa import Programa
from back_pez.db.model.componente import Componente
from back_pez.db.model.usuario import Usuario

from db.dbconfig import engine

router = APIRouter(prefix="/programa",
                   tags=["programa"],
                   responses={404: {"message": "No encontrado"}})

Session = sessionmaker(bind=engine)

@router.get("/")
async def programas():
    session = Session()
    programas = session.query(Programa).all()
    session.close()
    return programas

@router.get("/{id}")  # Path
async def programa(id: str):
    session = Session()
    programa = session.query(Programa).filter(Programa.id == id).first()
    session.close()
    if not programa:
        raise HTTPException(status_code=404, detail='Programa no encontrado')
    return programa

@router.post('/')
async def crear_programa(id: int,nombre: str, cantCreditos: int,componentes: List[Componente],usuarios: List[Usuario]):
    session = Session()
    nuevo_programa = Programa(id=id,nombre=nombre,cantCreditos=cantCreditos,componentes=componentes,usuarios=usuarios)
    session.add(nuevo_programa)
    session.commit()
    session.close()
    return nuevo_programa