from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import sessionmaker
from db.model.asignatura import Asignatura
from back_pez.db.model.actividad import Actividad
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
async def asignaturas():
    session = Session()
    asignaturas = session.query(Asignatura).all()
    session.close()
    return asignaturas

@router.get("/{id}")  # Path
async def asignatura(id: str):
    session = Session()
    asignatura = session.query(Asignatura).filter(Asignatura.id == id).first()
    session.close()
    if not asignatura:
        raise HTTPException(status_code=404, detail='Asignatura no encontrada')
    return asignatura

@router.post('/')
async def crear_asignatura(id: int,nombre: str, poblacionObjetivo: str, creditos:int, complejidad: str,
    modalidad: ComponenteClase, profesores: List[Profesor], modoEnsenianza: ModoEnsenianza,
    horarios: List[Horario], competencias: List[Competencia], actividades: List[Actividad], tematicas: List[Contenido]):
    session = Session()
    nueva_asignatura = Asignatura(id=id,nombre=nombre, poblacionObjetivo=poblacionObjetivo, creditos=creditos, complejidad=complejidad,
    modalidad=modalidad, profesores=profesores, modoEnsenianza=modoEnsenianza,horarios=horarios, 
    competencias=competencias, actividades=actividades, tematicas=tematicas)
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