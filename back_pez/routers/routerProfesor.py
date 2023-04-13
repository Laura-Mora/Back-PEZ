from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import sessionmaker
from back_pez.db.model.profesor import ProfesorModel
from db.model.profesor import Profesor
from db.dbconfig import engine
from sqlalchemy import insert

router = APIRouter(prefix="/profesor",
                   tags=["profesor"],
                   responses={404: {"message": "No encontrado"}})

Session = sessionmaker(bind=engine)

@router.get("/")
def profesores():
    session = Session()
    profesores = session.query(Profesor).all()
    session.close()
    return profesores

@router.get("/{id}")  # Path
def profesor(id: str):
    session = Session()
    profesor = session.query(Profesor).filter(Profesor.id == id).first()
    session.close()
    if not profesor:
        raise HTTPException(status_code=404, detail='Profesor no encontrado')
    return profesor


@router.post('/')
def crear_profesor(request:ProfesorModel):
    stmt = (
    insert(Profesor.__table__).
    values(id=request.id, nombre=request.nombre))
    return request

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