from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import sessionmaker
from back_pez.db.model.asignatura import AsignaturaModelo
from back_pez.db.model.subComponente import subComponenteModelo
from db.model.asignatura import Asignatura
from db.model.subComponente import subComponente

from db.dbconfig import engine

router = APIRouter(prefix="/componente",
                   tags=["componente"],
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
    session = Session()
    asiganturasOb_ids = [actividad.id for actividad in response.asignaturasObligatorias]
    asiganturasOb = session.query(Asignatura).filter(Asignatura.id.in_(asiganturasOb_ids)).all()
    asiganturasEl_ids = [actividad.id for actividad in response.asignaturasObligatorias]
    asiganturasEl = session.query(Asignatura).filter(Asignatura.id.in_(asiganturasEl_ids)).all()
    nuevo_subcomponente = subComponente(id=response.id,nombre=response.nombre, cantCreditos=response.cantCreditos,cantAsignaturas=response.cantAsignaturas,
    asignaturasObligatorias=asiganturasOb, asignaturasElectivas=asiganturasEl)
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