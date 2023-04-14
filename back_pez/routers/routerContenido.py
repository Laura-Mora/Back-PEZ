from fastapi import APIRouter, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.orm import sessionmaker
from back_pez.db.model.contenido import ContenidoModelo
from db.model.contenido import Contenido
from db.dbconfig import engine

router = APIRouter(prefix="/contenido",
                   tags=["contenido"],
                   responses={404: {"message": "No encontrado"}})

Session = sessionmaker(bind=engine)

@router.get("/")
def contenidos():
    print(select(Contenido.__table__))
    session = Session()
    contenidos = session.query(Contenido).all()
    session.close()
    return contenidos

@router.get("/{id}")  # Path
def contenido(id: str):
    session = Session()
    contenido = session.query(Contenido).filter(Contenido.id == id).first()
    session.close()
    if not contenido:
        raise HTTPException(status_code=404, detail='Contenido no encontrado')
    return contenido

@router.post('/')
def crear_contenido(request:ContenidoModelo):
    session = Session()
    contenido = Contenido(id=request.id, nombre=request.nombre)
    session.add(contenido)
    session.commit()
    session.close()
    return request 

@router.put('/{id}')
def actualizar_contenido(id: int, contenido_update: dict):
    session = Session()
    contenido = session.query(Contenido).filter(Contenido.id == id).first()
    if not contenido:
        raise HTTPException(status_code=404, detail='Competencia no encontrado')
    for campo, valor in contenido_update.items():
        setattr(contenido, campo, valor)
    session.add(contenido)
    session.commit()
    session.close()
    return contenido
