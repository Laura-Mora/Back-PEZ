from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import sessionmaker
from back_pez.db.model.horario import HorarioModel
from db.model.horario import Horario
from db.dbconfig import engine

from starlette.responses import Response

import datetime

router = APIRouter(prefix="/horario",
                   tags=["horario"],
                   responses={404: {"message": "No encontrado"}})

Session = sessionmaker(bind=engine)

@router.options("/")
def optionsHorarios():
    allowed_methods = ["GET", "OPTIONS","POST"]
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": ", ".join(allowed_methods),
        "Access-Control-Allow-Headers": "Content-Type, Accept"
    }
    return Response(headers=headers)

@router.get("/")
def horarios():
    session = Session()
    horarios = session.query(Horario).all()
    session.close()
    return horarios

@router.get("/{id}")  # Path
def horario(id: str):
    session = Session()
    horario = session.query(Horario).filter(Horario.id == id).first()
    session.close()
    if not horario:
        raise HTTPException(status_code=404, detail='Horario no encontrada')
    return horario

@router.post('/')
def crear_horario(request:HorarioModel):
    session = Session()
    nuevo_hoario = Horario(id=request.id, dia=request.dia, hora=request.hora)
    session.add(nuevo_hoario)
    session.commit()
    session.close()
    return nuevo_hoario 

@router.put('/{id}')
def actualizar_horario(id: int, horario_update: dict):
    session = Session()
    horario = session.query(Horario).filter(Horario.id == id).first()
    if not horario:
        raise HTTPException(status_code=404, detail='Horario no encontrado')
    for campo, valor in horario_update.items():
        setattr(horario, campo, valor)
    session.add(horario)
    session.commit()
    session.close()
    return horario
