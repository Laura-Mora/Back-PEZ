from typing import List
from fastapi import APIRouter, HTTPException, Request
from sqlalchemy.orm import sessionmaker
from back_pez.db.model.actividad import ActividadModelo
from db.model.actividad import Actividad
from db.dbconfig import engine
from sqlalchemy import insert

router = APIRouter(prefix="/actividad",
                   tags=["actividad"],
                   responses={404: {"message": "No encontrado"}})

Session = sessionmaker(bind=engine)

@router.get("/")
def actividades():
    session = Session()
    actividades = session.query(Actividad).all()
    session.close()
    return actividades

@router.get("/{id}")  # Path
def actividad(id: int):
    session = Session()
    actividad = session.query(Actividad).filter(Actividad.id == id).first()
    print(actividad)
    session.close()
    if not actividad:
        raise HTTPException(status_code=404, detail='Actividad no encontrada')
    return actividad

@router.post("/")
def crear_actividad(request: ActividadModelo):
    session = Session()
    actividad = Actividad(id=request.id, nombre=request.nombre)
    session.add(actividad)
    session.commit()
    session.close()
    return actividad 

@router.put('/{id}')
def actualizar_actividad(id: int, actividad_update: dict):
    session = Session()
    actividad = session.query(Actividad).filter(Actividad.id == id).first()
    if not actividad:
        raise HTTPException(status_code=404, detail='Actividad no encontrado')
    for campo, valor in actividad_update.items():
        setattr(actividad, campo, valor)
    session.add(actividad)
    session.commit()
    session.close()
    return actividad