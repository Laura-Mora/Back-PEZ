from typing import List

from fastapi import APIRouter, Body, HTTPException, Response
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from back_pez.db.model.usuario import Usuario
from back_pez.db.model.perfilEstudiante import PerfilEstudiante
from back_pez.db.model.actividad import Actividad, ActividadModelo
from back_pez.db.model.asignatura import Asignatura, AsignaturaModelo
from back_pez.db.model.competencia import Competencia, CompetenciaModel
from back_pez.db.model.componenteClase import ComponenteClase, ComponenteClaseModelo
from back_pez.db.model.tematica import Tematica, TematicaModelo
from back_pez.db.model.horario import Horario, HorarioModel
from back_pez.db.model.modoEnsenianza import ModoEnsenianza, ModoEnsenianzaModel
from negocio import negocioSugerenciaAsignatura, negocioSugerenciaPrograma

from db.dbconfig import engine
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/perfilEstudiante",
                   tags=["perfilEstudiante"],
                   responses={404: {"message": "No encontrado"}})

Session = sessionmaker(bind=engine)

@router.options("/")
def optionsUsuarios():
    allowed_methods = ["GET", "OPTIONS","POST"]
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": ", ".join(allowed_methods),
        "Access-Control-Allow-Headers": "Content-Type, Accept"
    }
    return Response(headers=headers)

@router.options("/{id}")
def optionsUsuarios():
    allowed_methods = ["GET", "OPTIONS","POST"]
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": ", ".join(allowed_methods),
        "Access-Control-Allow-Headers": "Content-Type, Accept"
    }
    return Response(headers=headers)

@router.options("/crear_perfil")
def optionsUsuarios():
    allowed_methods = ["GET", "OPTIONS","POST"]
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": ", ".join(allowed_methods),
        "Access-Control-Allow-Headers": "Content-Type, Accept"
    }
    return Response(headers=headers)

@router.options("/sugerenciaAsignatura/{id}")
def optionsSuges():
    allowed_methods = ["GET", "OPTIONS"]
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": ", ".join(allowed_methods),
        "Access-Control-Allow-Headers": "Content-Type, Accept"
    }
    return Response(headers=headers)

@router.options("/sugerenciaAsignaturaPreferencias/{id}")
def optionsSuges():
    allowed_methods = ["GET", "OPTIONS"]
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": ", ".join(allowed_methods),
        "Access-Control-Allow-Headers": "Content-Type, Accept"
    }
    return Response(headers=headers)

@router.options("/sugerenciaProgramaAsignaturas/{id}")
def optionsSugesPro():
    allowed_methods = ["GET", "OPTIONS"]
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": ", ".join(allowed_methods),
        "Access-Control-Allow-Headers": "Content-Type, Accept"
    }
    return Response(headers=headers)

@router.get("/")
def perfilesEstudiante():
    session = Session()
    perfiles = session.query(PerfilEstudiante).all()
    session.close()
    return perfiles

@router.get("/{id}")  # Path
def perfilEstudiante(id: str):
    session = Session()
    perfil = session.query(PerfilEstudiante).options(
        selectinload(PerfilEstudiante.asignaturasCursadas),
        selectinload(PerfilEstudiante.competenciasGusto),
        selectinload(PerfilEstudiante.horariosPreferencias),
        selectinload(PerfilEstudiante.modalidadPreferencia),
        selectinload(PerfilEstudiante.modoEnsenianzaPreferencia),
        selectinload(PerfilEstudiante.tematicasGusto)
        ).filter(PerfilEstudiante.id == id).first()
    session.close()
    if not perfil:
        raise HTTPException(status_code=404, detail='PerfilEstudiante no encontrado')
    return perfil


@router.post('/crear_perfil')
def crear_perfil(data: dict = Body(...)):
    try:
        idUsuario = data.get("idUsuario")
        profesion = data.get("profesion")
        areaDesempenio = data.get("areaDesempenio")
        motivo = data.get("motivo")
        javeriano = data.get("javeriano")
        ingles = data.get("ingles")
        semestre = data.get("semestre")
        id_asignaturas = data.get("asignaturasCursadas")
        id_tematicas = data.get("tematicasUsuario")
        id_competencias = data.get("competenciasUsuario")
        id_actividades = data.get("actividadesUsuario")
        id_horarios = data.get("horariosUsuario")
        id_modalidad = data.get("modalidadUsuario")
        id_modos = data.get("modosUsuario")
        session = Session()

        usuario_db = session.query(Usuario).filter(Usuario.id == idUsuario).first()

        if usuario_db.perfilEstudiante:
            perfil = usuario_db.perfilEstudiante
            perfil.profesion = profesion
            perfil.areaDesempenio = areaDesempenio
            perfil.motivacion = motivo
            perfil.javeriano = javeriano
            perfil.requisitoIngles = ingles
            perfil.semestre = semestre
            perfil.asignaturasCursadas = session.query(Asignatura).filter(Asignatura.id.in_(id_asignaturas)).all()
            perfil.modalidadPreferencia = session.query(ComponenteClase).filter(ComponenteClase.id.in_(id_modalidad)).all()
            perfil.modoEnsenianzaPreferencia = session.query(ModoEnsenianza).filter(ModoEnsenianza.id.in_(id_modos)).all()
            perfil.horariosPreferencias = session.query(Horario).filter(Horario.id.in_(id_horarios)).all()
            perfil.competenciasGusto = session.query(Competencia).filter(Competencia.id.in_(id_competencias)).all()
            perfil.actividadesGusto = session.query(Actividad).filter(Actividad.id.in_(id_actividades)).all()
            perfil.tematicasGusto = session.query(Tematica).filter(Tematica.id.in_(id_tematicas)).all()
            session.add(usuario_db)
            session.commit()
            session.close()
        else:

            cantidad_perfiles = session.query(func.count(PerfilEstudiante.id)).scalar()
            nuevo_id = cantidad_perfiles + 1

            asignaturas  = session.query(Asignatura).filter(Asignatura.id.in_(id_asignaturas)).all()
            tematicas  = session.query(Tematica).filter(Tematica.id.in_(id_tematicas)).all()
            competencias  = session.query(Competencia).filter(Competencia.id.in_(id_competencias)).all()
            actividades  = session.query(Actividad).filter(Actividad.id.in_(id_actividades)).all()
            hoarios  = session.query(Horario).filter(Horario.id.in_(id_horarios)).all()
            modalidades  = session.query(ComponenteClase).filter(ComponenteClase.id.in_(id_modalidad)).all()
            modos  = session.query(ModoEnsenianza).filter(ModoEnsenianza.id.in_(id_modos)).all()

            nuevo_perfil = PerfilEstudiante(
                id = nuevo_id,
                profesion = profesion,
                javeriano = javeriano,
                requisitoIngles = ingles,
                semestre = semestre,
                areaDesempenio = areaDesempenio,
                motivacion = motivo,
                asignaturasCursadas = asignaturas,
                modalidadPreferencia = modalidades,
                modoEnsenianzaPreferencia = modos,
                horariosPreferencias = hoarios,
                competenciasGusto = competencias,
                actividadesGusto = actividades,
                tematicasGusto = tematicas
            )

            session.add(nuevo_perfil)

            session.commit()
            session.close()

            session2 = Session()

            usuario_db = session2.query(Usuario).filter(Usuario.id == idUsuario).first()

            cantidad_perfiles2 = session2.query(func.count(PerfilEstudiante.id)).scalar()
            perfil = session2.query(PerfilEstudiante).filter(PerfilEstudiante.id == cantidad_perfiles2).first()
            
            usuario_db.perfilEstudiante = perfil
            usuario_db.perfilEstudiante_id = nuevo_id
            session2.add(usuario_db)

            session2.commit()
            session2.close()

        return usuario_db

    except Exception as e:
        print(f"Error: {e}")
        raise

    

@router.put('/{id}')
def actualizar_perfil(id: int, perfil_update: dict):
    session = Session()
    perfil = session.query(PerfilEstudiante).filter(PerfilEstudiante.id == id).first()
    if not perfil:
        raise HTTPException(status_code=404, detail='Perfil no encontrado')
    for campo, valor in perfil_update.items():
        setattr(perfil, campo, valor)
    session.add(perfil)
    session.commit()
    session.close()
    return perfil

@router.get("/sugerenciaAsignatura/{id}")
def sugerirAsignatura(id:int):
    return negocioSugerenciaAsignatura.recomendar_asignaturas(id)

@router.get("/sugerenciaAsignaturaPreferencias/{id}")
def sugerirAsignaturaPreferencias(id:int):
    return negocioSugerenciaAsignatura.sugerir_asignaturas_por_preferencias(id)

@router.get("/sugerenciaProgramaAsignaturas/{id}")
def sugerenciaProgramaAsignaturas(id: int):
    return negocioSugerenciaPrograma.recomendar_programas(id)