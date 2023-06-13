from typing import List

from fastapi import APIRouter, HTTPException, Response
from sqlalchemy.orm import sessionmaker
from db.model.programa import ProgramaModel
from db.model.programa import Programa
from db.model.componente import Componente, ComponenteModelo
from back_pez.db.model.usuario import Usuario

from db.dbconfig import engine

router = APIRouter(prefix="/programa",
                   tags=["programa"],
                   responses={404: {"message": "No encontrado"}})

Session = sessionmaker(bind=engine)

@router.options("/")
def optionsPrograma():
    allowed_methods = ["GET", "OPTIONS","POST"]
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": ", ".join(allowed_methods),
        "Access-Control-Allow-Headers": "Content-Type, Accept"
    }
    return Response(headers=headers)

@router.get("/")
def programas():
    session = Session()
    programas = session.query(Programa).all()
    session.close()
    return programas

@router.get("/{id}")  # Path
def programa(id: str):
    session = Session()
    programa = session.query(Programa).filter(Programa.id == id).first()
    session.close()
    if not programa:
        raise HTTPException(status_code=404, detail='Programa no encontrado')
    return programa

@router.post('/')
def crear_programa(response: ProgramaModel):
    session = Session()
    componentes_ids = [actividad.id for actividad in response.componentes]
    print("HOLA")
    componentes = session.query(Componente).filter(Componente.id.in_(componentes_ids)).all()
    nuevo_programa = Programa(id=response.id,nombre=response.nombre,cantCreditos=response.cantCreditos,componentes=componentes)
    session.add(nuevo_programa)
    session.commit()
    session.close()
    return nuevo_programa

@router.put('/{id}')
def actualizar_programa(id: int, programa_update: dict):
    session = Session()
    programa = session.query(Programa).filter(Programa.id == id).first()
    if not programa:
        raise HTTPException(status_code=404, detail='Programa no encontrado')
    for campo, valor in programa_update.items():
        setattr(programa, campo, valor)
    session.add(programa)
    session.commit()
    session.close()
    return programa