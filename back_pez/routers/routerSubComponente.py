from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import sessionmaker
from db.model.asignatura import Asignatura
from db.model.subComponente import subComponente

from db.dbconfig import engine

router = APIRouter(prefix="/componente",
                   tags=["componente"],
                   responses={404: {"message": "No encontrado"}})

Session = sessionmaker(bind=engine)

@router.get("/")
async def subComponentes():
    session = Session()
    subcomponentes = session.query(subComponente).all()
    session.close()
    return subcomponentes

@router.get("/{id}")  # Path
async def subcomponente(id: str):
    session = Session()
    subcomponente = session.query(subComponente).filter(Asignatura.id == id).first()
    session.close()
    if not subcomponente:
        raise HTTPException(status_code=404, detail='Subcomponente no encontrada')
    return subcomponente

@router.post('/')
async def crear_subcomponente(id: int,nombre: str, cantCreditos: int,cantAsignaturas: int,
    asignaturasObligatorias: List[Asignatura], asignaturasElectivas: List[Asignatura] ):
    session = Session()
    nuevo_subcomponente = subComponente(id=id,nombre=nombre, cantCreditos=cantCreditos,cantAsignaturas=cantAsignaturas,
    asignaturasObligatorias=asignaturasObligatorias, asignaturasElectivas=asignaturasElectivas)
    session.add(nuevo_subcomponente)
    session.commit()
    session.close()
    return nuevo_subcomponente

@router.put('/{id}')
def actualizar_subcomponente(id: int, subcomponente_update: dict):
    session = Session()
    subcomponente = session.query(subComponente).filter(subComponente.id == id).first()
    if not subcomponente:
        raise HTTPException(status_code=404, detail='SubComponente no encontrado')
    for campo, valor in subcomponente_update.items():
        setattr(subcomponente, campo, valor)
    session.add(subcomponente)
    session.commit()
    session.close()
    return subcomponente