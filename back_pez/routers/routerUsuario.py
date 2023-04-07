from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import sessionmaker
from db.model.usuario import Usuario
from back_pez.db.model.programa import ProgramaModel

from db.dbconfig import engine

router = APIRouter(prefix="/usuario",
                   tags=["usuario"],
                   responses={404: {"message": "No encontrado"}})

Session = sessionmaker(bind=engine)

@router.get("/")
def usuarios():
    session = Session()
    usuaruios = session.query(Usuario).all()
    session.close()
    return usuaruios

@router.get("/{id}")  # Path
def usuario(id: str):
    session = Session()
    usuario = session.query(Usuario).filter(Usuario.id == id).first()
    session.close()
    if not usuario:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    return usuario

@router.post('/')
def crear_usuario(id: int,nombre: str, correo: str, contrasenia: str,
    programa: List[ProgramaModel], tipo:str):
    session = Session()
    nuevo_usuario = Usuario(id=id,nombre=nombre,correo=correo, contrasenia=contrasenia,programa= programa, tipo=tipo)
    session.add(nuevo_usuario)
    session.commit()
    session.close()
    return nuevo_usuario

@router.put('/{id}')
def actualizar_usuario(id: int, usuario_update: dict):
    session = Session()
    usuario = session.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    for campo, valor in usuario_update.items():
        setattr(usuario, campo, valor)
    session.add(usuario)
    session.commit()
    session.close()
    return usuario