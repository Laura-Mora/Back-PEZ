from typing import List
from urllib import response
from fastapi import APIRouter, HTTPException, Response
from sqlalchemy.orm import sessionmaker
from back_pez.db.model.componente import ComponenteElectiva, ComponenteObligactoria, ComponenteSubComponente
from db.model.componente import ComponenteModelo
from db.model.componente import Componente
from back_pez.db.model.asignatura import Asignatura, AsignaturaModelo
from back_pez.db.model.subComponente import subComponente, subComponenteModelo
from sqlalchemy.orm import selectinload

from negocio import negocioComponente

from db.dbconfig import engine

router = APIRouter(prefix="/componente",
                   tags=["componente"],
                   responses={404: {"message": "No encontrado"}})

Session = sessionmaker(bind=engine)

@router.options("/")
def optionsComponentes():
    allowed_methods = ["GET", "OPTIONS","POST"]
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": ", ".join(allowed_methods),
        "Access-Control-Allow-Headers": "Content-Type, Accept"
    }
    return Response(headers=headers)

@router.options("/{id}")
def optionsComponente():
    allowed_methods = ["GET", "OPTIONS","POST"]
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": ", ".join(allowed_methods),
        "Access-Control-Allow-Headers": "Content-Type, Accept"
    }
    return Response(headers=headers)

@router.get("/")
def componentes():
    session = Session()
    componentes = session.query(Componente).all()
    session.close()
    return componentes

@router.get("/{id}")  # Path
def componentes(id: str):
    session = Session()
    componente = session.query(Componente).filter(Componente.id == id).first()
    
    if not componente:
        raise HTTPException(status_code=404, detail='Componente no encontrado')
    
    asiganturasOb = (
        session.query(ComponenteObligactoria).options(
        selectinload(ComponenteObligactoria.asignaturasObligatorias))
        .filter(ComponenteObligactoria.componente_id == componente.id)
        .first()
    )


    asignaturas_electivas = (
        session.query(ComponenteElectiva).options(
        selectinload(ComponenteElectiva.asignaturasElectivas)
        ).filter(ComponenteElectiva.componente_id == id)
        .first()
    )

    subcomponentes = (
        session.query(ComponenteSubComponente).options(
        selectinload(ComponenteSubComponente.subcomponentes)
        ).filter(ComponenteSubComponente.componente_id == id)
        .first()
    )
    
    session.close()
    
    componente_data = {
        "id": componente.id,
        "nombre": componente.nombre,
        "cantCreditos": componente.cantCreditos,
        "asignaturasObligatorias": asiganturasOb,
        "asignaturasElectivas": asignaturas_electivas,
        "subcomponentes": subcomponentes,
    }

    return componente_data

@router.post("/")
def crear_componente(response:ComponenteModelo):
    return negocioComponente.crear_componente(response)
    

@router.put("/{id}")
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