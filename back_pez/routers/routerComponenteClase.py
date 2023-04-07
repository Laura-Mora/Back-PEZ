from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import sessionmaker
from db.model.componenteClase import ComponenteClase
from db.dbconfig import engine

router = APIRouter(prefix="/componenteClase",
                   tags=["componenteClase"],
                   responses={404: {"message": "No encontrado"}})

Session = sessionmaker(bind=engine)

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
def crear_modalidad(id: int,nombre: str):
    session = Session()
    nuevo_modalidad = ComponenteClase(id=id,nombre=nombre)
    session.add(nuevo_modalidad)
    session.commit()
    session.close()
    return nuevo_modalidad

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