from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import sessionmaker
from db.model.componenteClase import ComponenteClase
from db.dbconfig import engine

router = APIRouter(prefix="/componenteClase",
                   tags=["componenteClase"],
                   responses={404: {"message": "No encontrado"}})

Session = sessionmaker(bind=engine)

@router.get("/")
async def componentesClase():
    session = Session()
    modalidades = session.query(ComponenteClase).all()
    session.close()
    return modalidades

@router.get("/{id}")  # Path
async def componenteClase(id: str):
    session = Session()
    modalidad = session.query(ComponenteClase).filter(ComponenteClase.id == id).first()
    session.close()
    if not modalidad:
        raise HTTPException(status_code=404, detail='ComponenteClase no encontrado')
    return modalidad


@router.post('/')
async def crear_modo(id: int,nombre: str):
    session = Session()
    nuevo_modalidad = ComponenteClase(id=id,nombre=nombre)
    session.add(nuevo_modalidad)
    session.commit()
    session.close()
    return nuevo_modalidad