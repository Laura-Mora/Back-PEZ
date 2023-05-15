from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import sessionmaker
from db.model.asignatura import AsignaturaModelo
from db.model.subComponente import subComponenteModelo
from db.model.asignatura import Asignatura
from db.model.subComponente import subComponente

from db.dbconfig import engine

from pprint import pprint

router = APIRouter(prefix="/subcomponente",
                   tags=["subcomponente"],
                   responses={404: {"message": "No encontrado"}})

Session = sessionmaker(bind=engine)

@router.get("/")
def subComponentes():
    session = Session()
    subcomponentes = session.query(subComponente).all()
    session.close()
    return subcomponentes

@router.get("/{id}")  # Path
def subcomponente(id: str):
    session = Session()
    subcomponente = session.query(subComponente).filter(subComponente.id == id).first()
    session.close()
    if not subcomponente:
        raise HTTPException(status_code=404, detail='Subcomponente no encontrada')
    return subcomponente

@router.post('/')
def crear_subcomponente(response: subComponenteModelo):
    print(response)
    session = Session()
    asiganturasOb = []
    asiganturasEl = []
    nuevo_subcomponente = None

    if response.asignaturasObligatorias:
        asiganturasOb_ids = [asignatura.id for asignatura in response.asignaturasObligatorias]
        asiganturasOb = session.query(Asignatura).filter(Asignatura.id.in_(asiganturasOb_ids)).all()
    if response.asignaturasElectivas:
        asiganturasEl_ids = [asignatura.id for asignatura in response.asignaturasElectivas]
        asiganturasEl = session.query(Asignatura).filter(Asignatura.id.in_(asiganturasEl_ids)).all()

    """if asiganturasOb and asiganturasEl:
        nuevo_subcomponente = subComponente(id=response.id,nombre=response.nombre, cantCreditos=response.cantCreditos,cantAsignaturas=response.cantAsignaturas,
        asignaturasObligatorias=asiganturasOb, asignaturasElectivas=asiganturasEl)
    elif asiganturasEl:
        nuevo_subcomponente = subComponente(id=response.id,nombre=response.nombre, cantCreditos=response.cantCreditos,cantAsignaturas=response.cantAsignaturas,
        asignaturasElectivas=asiganturasEl)    
    elif asiganturasOb:
        nuevo_subcomponente = subComponente(id=response.id,nombre=response.nombre, cantCreditos=response.cantCreditos,cantAsignaturas=response.cantAsignaturas,
        asignaturasObligatorias=asiganturasOb)"""
    
    nuevo_subcomponente = subComponente(id=response.id,nombre=response.nombre, cantCreditos=response.cantCreditos,cantAsignaturas=response.cantAsignaturas,
        asignaturasObligatorias=asiganturasOb, asignaturasElectivas=asiganturasEl)
    pprint(vars(nuevo_subcomponente))
    session.add(nuevo_subcomponente)
    print("VOY BIEN")
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