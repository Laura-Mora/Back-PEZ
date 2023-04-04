from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import sessionmaker
from db.model.contenido import Contenido
from db.dbconfig import engine

router = APIRouter(prefix="/contenido",
                   tags=["contenido"],
                   responses={404: {"message": "No encontrado"}})

Session = sessionmaker(bind=engine)

@router.get("/")
async def contenidos():
    session = Session()
    contenidos = session.query(Contenido).all()
    session.close()
    return contenidos

@router.get("/{id}")  # Path
async def contenido(id: str):
    session = Session()
    contenido = session.query(Contenido).filter(Contenido.id == id).first()
    session.close()
    if not contenido:
        raise HTTPException(status_code=404, detail='Contenido no encontrado')
    return contenido

@router.post('/')
async def crear_contenido(id: int,nombre: str):
    session = Session()
    nuevo_contenido = Contenido(id=id,nombre=nombre)
    session.add(nuevo_contenido)
    session.commit()
    session.close()
    return nuevo_contenido

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
