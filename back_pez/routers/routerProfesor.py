from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import sessionmaker
from db.model.profesor import Profesor
from db.dbconfig import engine

router = APIRouter(prefix="/profesor",
                   tags=["profesor"],
                   responses={404: {"message": "No encontrado"}})

Session = sessionmaker(bind=engine)

@router.get("/")
async def profesores():
    session = Session()
    profesores = session.query(Profesor).all()
    session.close()
    return profesores

@router.get("/{id}")  # Path
async def profesor(id: str):
    session = Session()
    profesor = session.query(Profesor).filter(Profesor.id == id).first()
    session.close()
    if not profesor:
        raise HTTPException(status_code=404, detail='Profesor no encontrado')
    return profesor


@router.post('/')
async def crear_profesor(id: int,nombre: str):
    session = Session()
    nuevo_profesor = Profesor(id=id,nombre=nombre)
    session.add(nuevo_profesor)
    session.commit()
    session.close()
    return nuevo_profesor

@router.put('/{id}')
def actualizar_perfil(id: int, profesor_update: dict):
    session = Session()
    profesor = session.query(Profesor).filter(Profesor.id == id).first()
    if not profesor:
        raise HTTPException(status_code=404, detail='Profesor no encontrado')
    for campo, valor in profesor_update.items():
        setattr(profesor, campo, valor)
    session.add(profesor)
    session.commit()
    session.close()
    return profesor