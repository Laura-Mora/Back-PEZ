from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import sessionmaker
from back_pez.db.model.actividad import Actividad
from back_pez.db.model.asignatura import Asignatura, AsignaturaModelo
from back_pez.db.model.competencia import Competencia
from back_pez.db.model.componenteClase import ComponenteClase
from back_pez.db.model.contenido import Contenido
from back_pez.db.model.horario import Horario
from back_pez.db.model.modoEnsenianza import ModoEnsenianza
from back_pez.db.model.profesor import Profesor

from db.dbconfig import engine


router = APIRouter(prefix="/asignatura",
                   tags=["asignatura"],
                   responses={404: {"message": "No encontrado"}})

Session = sessionmaker(bind=engine)

@router.get("/")
def getAsignaturas():
    session = Session()
    asignaturas = session.query(Asignatura).all()
    session.close()
    return asignaturas

@router.get("/{id}")  # Path
def getAsignatura(id: str):
    session = Session()
    asignatura = session.query(Asignatura).filter(Asignatura.id == id).first()
    session.close()
    if not asignatura:
        raise HTTPException(status_code=404, detail='Asignatura no encontrada')
    return asignatura

@router.post('/')
def crear_asignatura(request:AsignaturaModelo):
    session = Session()
    nueva_asignatura = Asignatura(id=request.id,nombre=request.nombre, poblacionObjetivo=request.poblacionObjetivo, creditos=request.creditos, complejidad=request.complejidad,
    modalidad=request.modalidad, profesores=request.profesores, modoEnsenianza=request.modoEnsenianza,horarios=request.horarios, 
    competencias=request.competencias, actividades=request.actividades, tematicas=request.tematicas)
    session.add(nueva_asignatura)
    session.commit()
    session.close()
    return nueva_asignatura

@router.put('/{id}')
def actualizar_asignatura(id: int, asignatura_update: dict):
    session = Session()
    asignatura = session.query(Asignatura).filter(Asignatura.id == id).first()
    if not asignatura:
        raise HTTPException(status_code=404, detail='Asignatura no encontrado')
    for campo, valor in asignatura_update.items():
        setattr(asignatura, campo, valor)
    session.add(asignatura)
    session.commit()
    session.close()
    return asignatura