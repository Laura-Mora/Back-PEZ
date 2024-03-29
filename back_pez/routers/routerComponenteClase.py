from fastapi import APIRouter, HTTPException, Response
from sqlalchemy.orm import sessionmaker
from back_pez.db.model.componenteClase import ComponenteClaseModelo
from db.model.componenteClase import ComponenteClase
from db.dbconfig import engine
from sqlalchemy import insert

router = APIRouter(prefix="/componenteClase",
                   tags=["componenteClase"],
                   responses={404: {"message": "No encontrado"}})

Session = sessionmaker(bind=engine)

@router.options("/")
def optionsComponenteClase():
    allowed_methods = ["GET", "OPTIONS","POST"]
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": ", ".join(allowed_methods),
        "Access-Control-Allow-Headers": "Content-Type, Accept"
    }
    return Response(headers=headers)

@router.get("/")
def componentesClase():
    session = Session()
    modalidades = session.query(ComponenteClase).all()
    session.close()
    return modalidades

@router.get("/{id}")  # Path
def componenteClase(id: str):
    session = Session()
    modalidad = session.query(ComponenteClase).filter(ComponenteClase.id == id).first()
    session.close()
    if not modalidad:
        raise HTTPException(status_code=404, detail='ComponenteClase no encontrado')
    return modalidad


@router.post('/')
def crear_modalidad(request:ComponenteClaseModelo):
    session = Session()
    componente = ComponenteClase(id=request.id, nombre=request.nombre)
    session.add(componente)
    session.commit()
    session.close()
    return componente

@router.put('/{id}')
def actualizar_modalidad(id: int, modalidad_update: dict):
    session = Session()
    modalidad = session.query(ComponenteClase).filter(ComponenteClase.id == id).first()
    if not modalidad:
        raise HTTPException(status_code=404, detail='Competencia no encontrado')
    for campo, valor in modalidad_update.items():
        setattr(modalidad, campo, valor)
    session.add(modalidad)
    session.commit()
    session.close()
    return modalidad