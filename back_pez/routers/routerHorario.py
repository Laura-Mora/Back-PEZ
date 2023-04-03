from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import sessionmaker
from db.model.horario import Horario
from db.dbconfig import engine

import datetime

router = APIRouter(prefix="/horario",
                   tags=["horario"],
                   responses={404: {"message": "No encontrado"}})

Session = sessionmaker(bind=engine)

@router.get("/")
async def horarios():
    session = Session()
    horarios = session.query(Horario).all()
    session.close()
    return horarios

@router.get("/{id}")  # Path
async def horario(id: str):
    session = Session()
    horario = session.query(Horario).filter(Horario.id == id).first()
    session.close()
    if not horario:
        raise HTTPException(status_code=404, detail='Horario no encontrada')
    return horario

@router.post('/')
async def crear_horario(id: int,dia: str, hora:datetime.time):
    session = Session()
    nuevo_hoario = Horario(id=id, dia=dia, hora=hora)
    session.add(nuevo_hoario)
    session.commit()
    session.close()
    return nuevo_hoario 