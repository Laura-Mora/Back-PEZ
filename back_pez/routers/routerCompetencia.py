from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import sessionmaker
from db.model.competencia import Competencia

from db.dbconfig import engine

router = APIRouter(prefix="/competencia",
                   tags=["competencia"],
                   responses={404: {"message": "No encontrado"}})

Session = sessionmaker(bind=engine)

@router.get("/")
async def competencias():
    session = Session()
    competencias = session.query(Competencia).all()
    session.close()
    return competencias

@router.get("/{id}")  # Path
async def competencia(id: str):
    session = Session()
    competencia = session.query(Competencia).filter(Competencia.id == id).first()
    session.close()
    if not competencia:
        raise HTTPException(status_code=404, detail='Competencia no encontrado')
    return competencia


@router.post('/')
async def crear_competencia(id: int,nombre: str):
    session = Session()
    nueva_competencia = Competencia(id=id,nombre=nombre)
    session.add(nueva_competencia)
    session.commit()
    session.close()
    return nueva_competencia