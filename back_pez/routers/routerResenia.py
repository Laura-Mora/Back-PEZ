from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import sessionmaker
from back_pez.db.model.asignatura import Asignatura
from db.model.reseniaAsignatura import ReseniaAsignatura

from db.dbconfig import engine

router = APIRouter(prefix="/resenia",
                   tags=["resenia"],
                   responses={404: {"message": "No encontrado"}})

Session = sessionmaker(bind=engine)

@router.get("/")
async def resenias():
    session = Session()
    resenias = session.query(ReseniaAsignatura).all()
    session.close()
    return resenias

@router.get("/{id}")  # Path
async def resenia(id: str):
    session = Session()
    resenia = session.query(ReseniaAsignatura).filter(ReseniaAsignatura.id == id).first()
    session.close()
    if not resenia:
        raise HTTPException(status_code=404, detail='Reseña no encontrado')
    return resenia

@router.post('/')
async def crear_resenia(id: int, aprendizaje: bool, tematicaRequeridas: bool, estrategiasPedagogicasProfesor: bool,
    actividadesAsignatura: bool, complejidad: str, agradoProfesor: bool, vidaOTrabajo: str, cargaAsigantura: bool,
    nivelExigencia: str, entregaNotas: bool, retroalimentacion: bool, comentarios: str, incidenciaProfesor: str,
    asignatura: Asignatura):
    session = Session()
    nuevo_resenia = ReseniaAsignatura(id=id,aprendizaje=aprendizaje, tematicaRequeridas=tematicaRequeridas, estrategiasPedagogicasProfesor=estrategiasPedagogicasProfesor,
    actividadesAsignatura=actividadesAsignatura, complejidad=complejidad, agradoProfesor=agradoProfesor, vidaOTrabajo=vidaOTrabajo, cargaAsigantura=cargaAsigantura,
    nivelExigencia=nivelExigencia, entregaNotas=entregaNotas, retroalimentacion=retroalimentacion, comentarios=comentarios, incidenciaProfesor=incidenciaProfesor,
    asignatura=asignatura)
    session.add(nuevo_resenia)
    session.commit()
    session.close()
    return nuevo_resenia

@router.put('/{id}')
def actualizar_resenia(id: int, resenia_update: dict):
    session = Session()
    resenia = session.query(ReseniaAsignatura).filter(ReseniaAsignatura.id == id).first()
    if not resenia:
        raise HTTPException(status_code=404, detail='Reseña no encontrado')
    for campo, valor in resenia_update.items():
        setattr(resenia, campo, valor)
    session.add(resenia)
    session.commit()
    session.close()
    return resenia