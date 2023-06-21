from typing import List

from fastapi import APIRouter, Body, HTTPException, Response
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from back_pez.db.model.asignatura import Asignatura
from db.model.reseniaAsignatura import ReseniaAsignatura

from db.dbconfig import engine

router = APIRouter(prefix="/resenia",
                   tags=["resenia"],
                   responses={404: {"message": "No encontrado"}})

Session = sessionmaker(bind=engine)

@router.options("/")
def optionsResenia():
    allowed_methods = ["GET", "OPTIONS","POST"]
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": ", ".join(allowed_methods),
        "Access-Control-Allow-Headers": "Content-Type, Accept"
    }
    return Response(headers=headers)

@router.options("/crear_resenia")
def optionsReseniaCrear():
    allowed_methods = [ "OPTIONS","POST"]
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": ", ".join(allowed_methods),
        "Access-Control-Allow-Headers": "Content-Type, Accept"
    }
    return Response(headers=headers)

@router.get("/")
def resenias():
    session = Session()
    resenias = session.query(ReseniaAsignatura).all()
    session.close()
    return resenias

@router.get("/{id}")  # Path
def resenia(id: str):
    session = Session()
    resenia = session.query(ReseniaAsignatura).filter(ReseniaAsignatura.id == id).first()
    session.close()
    if not resenia:
        raise HTTPException(status_code=404, detail='Reseña no encontrado')
    return resenia

@router.post("/crear_resenia")
def crear_resenia(data: dict = Body(...)):
    try:
        aprendizaje = data.get("aprendizaje")
        tematicaRequeridas = data.get("tematicasAbordadas")
        estrategiasPedagogicasProfesor = data.get("estrategiasPedagogicasProfesor")
        actividadesAsignatura = data.get("actividadesAsignatura")
        complejidad = data.get("complejidad")
        agradoProfesor = data.get("agradoProfesor")
        vidaOTrabajo = data.get("vidaOTrabajo")
        cargaAsigantura = data.get("cargaAsignatura")
        nivelExigencia = data.get("nivelExigencia")
        entregaNotas = data.get("entregaNotas")
        retroalimentacion = data.get("retroalimentacion")
        comentarios = data.get("comentarios")
        incidenciaProfesor = data.get("incidenciaProfesor")
        asignatura_id = data.get("asignatura_id")
        
        session = Session()
        cantidad_resenia = session.query(func.count(ReseniaAsignatura.id)).scalar()
        nuevo_id = cantidad_resenia + 1

        asignatura = session.query(Asignatura).filter(Asignatura.id == asignatura_id).first()
        
        nuevo_resenia = ReseniaAsignatura(
            id=nuevo_id,
            aprendizaje=aprendizaje, 
            tematicaRequeridas=tematicaRequeridas, 
            estrategiasPedagogicasProfesor=estrategiasPedagogicasProfesor,
            actividadesAsignatura=actividadesAsignatura, 
            complejidad=complejidad, 
            agradoProfesor=agradoProfesor, 
            vidaOTrabajo=vidaOTrabajo, 
            cargaAsigantura=cargaAsigantura,
            nivelExigencia=nivelExigencia, 
            entregaNotas=entregaNotas, 
            retroalimentacion=retroalimentacion, 
            comentarios=comentarios, 
            incidenciaProfesor=incidenciaProfesor,
            asignatura=asignatura)
        
        session.add(nuevo_resenia)
        session.commit()
        session.close()
        return nuevo_resenia
    except Exception as e:
        print(f"Error: {e}")
        raise

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