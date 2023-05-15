from fastapi import APIRouter, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.orm import sessionmaker
from back_pez.db.model.tematica import TematicaModelo
from db.model.tematica import Tematica
from db.dbconfig import engine

router = APIRouter(prefix="/tematica",
                   tags=["tematica"],
                   responses={404: {"message": "No encontrado"}})

Session = sessionmaker(bind=engine)

@router.get("/")
def contenidos():
    print(select(Tematica.__table__))
    session = Session()
    contenidos = session.query(Tematica).all()
    session.close()
    return contenidos

@router.get("/{id}")  # Path
def contenido(id: str):
    session = Session()
    contenido = session.query(Tematica).filter(Tematica.id == id).first()
    session.close()
    if not contenido:
        raise HTTPException(status_code=404, detail='Tematica no encontrado')
    return contenido

@router.post('/')
def crear_contenido(request:TematicaModelo):
    session = Session()
    contenido = Tematica(id=request.id, nombre=request.nombre)
    session.add(contenido)
    session.commit()
    session.close()
    return request 

@router.put('/{id}')
def actualizar_contenido(id: int, contenido_update: dict):
    session = Session()
    contenido = session.query(Tematica).filter(Tematica.id == id).first()
    if not contenido:
        raise HTTPException(status_code=404, detail='Tematica no encontrado')
    for campo, valor in contenido_update.items():
        setattr(contenido, campo, valor)
    session.add(contenido)
    session.commit()
    session.close()
    return contenido
