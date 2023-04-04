from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import sessionmaker
from db.model.usuario import Usuario
from back_pez.db.model.programa import Programa

from db.dbconfig import engine

router = APIRouter(prefix="/usuario",
                   tags=["usuario"],
                   responses={404: {"message": "No encontrado"}})

Session = sessionmaker(bind=engine)

@router.get("/")
async def usuarios():
    session = Session()
    usuaruios = session.query(Usuario).all()
    session.close()
    return usuaruios

@router.get("/{id}")  # Path
async def usuario(id: str):
    session = Session()
    usuario = session.query(Usuario).filter(Usuario.id == id).first()
    session.close()
    if not usuario:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    return usuario

@router.post('/')
async def crear_usuario(id: int,nombre: str, correo: str, contrasenia: str,
    programa: List[Programa], tipo:str):
    session = Session()
    nuevo_usuario = Usuario(id=id,nombre=nombre,correo=correo, contrasenia=contrasenia,programa= programa, tipo=tipo)
    session.add(nuevo_usuario)
    session.commit()
    session.close()
    return nuevo_usuario