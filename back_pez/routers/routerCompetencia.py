from fastapi import APIRouter, HTTPException, Response
from sqlalchemy.orm import sessionmaker
from back_pez.db.model.competencia import CompetenciaModel
from db.model.competencia import Competencia

from db.dbconfig import engine

router = APIRouter(prefix="/competencia",
                   tags=["competencia"],
                   responses={404: {"message": "No encontrado"}})

Session = sessionmaker(bind=engine)

@router.options("/")
def optionsCompetencias():
    allowed_methods = ["GET", "OPTIONS","POST"]
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": ", ".join(allowed_methods),
        "Access-Control-Allow-Headers": "Content-Type, Accept"
    }
    return Response(headers=headers)

@router.get("/")
def competencias():
    session = Session()
    competencias = session.query(Competencia).all()
    session.close()
    return competencias

@router.get("/{id}")  # Path
def competencia(id: str):
    session = Session()
    competencia = session.query(Competencia).filter(Competencia.id == id).first()
    session.close()
    if not competencia:
        raise HTTPException(status_code=404, detail='Competencia no encontrado')
    return competencia


@router.post('/')
def crear_competencia(request:CompetenciaModel):
    session = Session()
    nueva_competencia = Competencia(id=request.id,nombre=request.nombre)
    session.add(nueva_competencia)
    session.commit()
    session.close()
    return request

@router.put('/{id}')
def actualizar_competencia(id: int, competencia_update: dict):
    session = Session()
    competencia = session.query(Competencia).filter(Competencia.id == id).first()
    if not competencia:
        raise HTTPException(status_code=404, detail='Competencia no encontrado')
    for campo, valor in competencia_update.items():
        setattr(competencia, campo, valor)
    session.add(competencia)
    session.commit()
    session.close()
    return competencia