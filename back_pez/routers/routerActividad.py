from typing import List
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import sessionmaker
from db.model.actividad import Actividad
from db.dbconfig import engine

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
    session.close()
    if not actividad:
        raise HTTPException(status_code=404, detail='Actividad no encontrada')
    return actividad

@router.post('/')
def crear_actividad(id: int,nombre: str):
    session = Session()
    nueva_actividad = Actividad(id=id,nombre=nombre)
    session.add(nueva_actividad)
    session.commit()
    session.close()
    return nueva_actividad 

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