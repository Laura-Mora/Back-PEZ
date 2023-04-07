from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import sessionmaker
from db.model.modoEnsenianza import ModoEnsenianza
from db.dbconfig import engine

router = APIRouter(prefix="/modoEnsenianza",
                   tags=["modoEnsenianza"],
                   responses={404: {"message": "No encontrado"}})

Session = sessionmaker(bind=engine)

@router.get("/")
def modosEnsenianza():
    session = Session()
    modos = session.query(ModoEnsenianza).all()
    session.close()
    return modos

@router.get("/{id}")  # Path
def modoEnsenianza(id: str):
    session = Session()
    modo = session.query(ModoEnsenianza).filter(ModoEnsenianza.id == id).first()
    session.close()
    if not modo:
        raise HTTPException(status_code=404, detail='Modo de enseñanza no encontrado')
    return modo


@router.post('/')
def crear_modo(id: int,nombre: str):
    session = Session()
    nuevo_modo = ModoEnsenianza(id=id,nombre=nombre)
    session.add(nuevo_modo)
    session.commit()
    session.close()
    return nuevo_modo

@router.put('/{id}')
def actualizar_modo(id: int, modo_update: dict):
    session = Session()
    modo = session.query(ModoEnsenianza).filter(ModoEnsenianza.id == id).first()
    if not modo:
        raise HTTPException(status_code=404, detail='Modo no encontrado')
    for campo, valor in modo_update.items():
        setattr(modo, campo, valor)
    session.add(modo)
    session.commit()
    session.close()
    return modo