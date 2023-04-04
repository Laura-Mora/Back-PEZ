from typing import List
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import sessionmaker
from db.model.componente import Componente
from back_pez.db.model.asignatura import Asignatura
from back_pez.db.model.subComponente import subComponente

from db.dbconfig import engine

router = APIRouter(prefix="/componente",
                   tags=["componente"],
                   responses={404: {"message": "No encontrado"}})

Session = sessionmaker(bind=engine)

@router.get("/")
async def componentes():
    session = Session()
    componentes = session.query(Componente).all()
    session.close()
    return componentes

@router.get("/{id}")  # Path
async def componentes(id: str):
    session = Session()
    componente = session.query(Componente).filter(Componente.id == id).first()
    session.close()
    if not componente:
        raise HTTPException(status_code=404, detail='Componente no encontrado')
    return componente

@router.post('/')
async def crear_componente(id: int,nombre: str, asignaturasObligatorias:List[Asignatura],
    asignaturasElectivas: List[Asignatura], subcomponentes:List[subComponente]):
    session = Session()
    nuevo_componente = Componente(id=id,nombre=nombre,asignaturasObligatorias=asignaturasObligatorias,asignaturasElectivas=asignaturasElectivas,subcomponentes=subcomponentes)
    session.add(nuevo_componente)
    session.commit()
    session.close()
    return nuevo_componente

@router.put('/{id}')
def actualizar_componente(id: int, componente_update: dict):
    session = Session()
    componente = session.query(Componente).filter(Componente.id == id).first()
    if not componente:
        raise HTTPException(status_code=404, detail='Competencia no encontrado')
    for campo, valor in componente_update.items():
        setattr(componente, campo, valor)
    session.add(componente)
    session.commit()
    session.close()
    return componente