from sqlalchemy.orm import sessionmaker
from back_pez.db.model.asignatura import Asignatura
from back_pez.db.model.componente import Componente, ComponenteElectiva, ComponenteObligactoria, ComponenteSubComponente
from back_pez.db.model.perfilEstudiante import PerfilEstudiante
from back_pez.db.model.programa import Programa
from back_pez.db.model.subComponente import subComponente
from back_pez.db.model.usuario import Usuario
from db.dbconfig import engine
from sqlalchemy import exists

from sqlalchemy.orm import selectinload

Session = sessionmaker(bind=engine)

import json

def recomendar_programas(estudiante_id):
    try:
        session = Session()
        programas = session.query(Programa).all()

        usuario = session.query(Usuario).options(
        selectinload(Usuario.programa)
        ).filter(Usuario.id == estudiante_id).first()


        estudiante = session.query(PerfilEstudiante).options(
        selectinload(PerfilEstudiante.asignaturasCursadas)
        ).filter(PerfilEstudiante.id == usuario.perfilEstudiante_id).first()

        asignaturas_aprobadas = estudiante.asignaturasCursadas

        programas_recomendados = []

        programas_disponibles = [programa for programa in programas if programa not in usuario.programa]

        for programa in programas_disponibles:
            print("-----------------")
            print(programa.nombre)

            asignaturas_requeridas = []
            asignaturas_requeridas = obtener_asignaturas_requeridas_programa(programa.id)

            asignaturas_aprobadas_programa = set()

            for asigPro in asignaturas_requeridas:
                print(asigPro.nombre)
                for asignatura in asignaturas_aprobadas:
                    if asignatura.nombre == asigPro.nombre:
                        asignaturas_aprobadas_programa.add(asignatura)


            if len(asignaturas_aprobadas_programa) > 0 :
                programa_recomendado = {
                    'nombre_programa': programa.nombre,
                    'asignaturas_aprobadas': list(asignaturas_aprobadas_programa),
                }
                programas_recomendados.append(programa)

        return programas_recomendados

    except Exception as error:
        print(f"Error en recomendar_programas: {error}")
        return None


def obtener_asignaturas_requeridas_programa(programa_id):

    asignaturas_requeridas = []
    subcomponentes = []

    componentes = obtener_componentes_programa(programa_id)

    for componente in componentes:
        subcomponentes.extend(obtener_subcomponentes_componente(componente.id))
        asignaturas_requeridas.extend(obtener_asignaturasOB_componente(componente.id))
        asignaturas_requeridas.extend(obtener_asignaturasEle_componente(componente.id))

    for subcomponete in subcomponentes:
        asignaturas_requeridas.extend(obtener_asignaturasOB_subcomponente(subcomponete.id))
        asignaturas_requeridas.extend(obtener_asignaturasEle_subcomponente(subcomponete.id))

    return asignaturas_requeridas

def obtener_componentes_programa(programa_id):
    session = Session()
    programa = session.query(Programa).options(
        selectinload(Programa.componentes)).filter(Programa.id == programa_id).first()
    componentes = programa.componentes
    session.close()

    return componentes

def obtener_subcomponentes_componente(componente_id):
    session = Session()

    componente_subcomponente = (
        session.query(ComponenteSubComponente)
        .filter(ComponenteSubComponente.componente_id == componente_id)
        .first()
    )

    if componente_subcomponente:
        subcomponentes = componente_subcomponente.subcomponentes
    else:
        subcomponentes = []

    session.close()

    return subcomponentes

def  obtener_asignaturasOB_subcomponente(subcomponente_id):
    session = Session()
    subcomponete = session.query(subComponente).options(
        selectinload(subComponente.asignaturasObligatorias)
        ).filter(subComponente.id == subcomponente_id).first()
    asignaturasObligatorias = subcomponete.asignaturasObligatorias

    session.close()
    return asignaturasObligatorias

def  obtener_asignaturasEle_subcomponente(subcomponente_id):
    session = Session()
    subcomponete = session.query(subComponente).options(
        selectinload(subComponente.asignaturasElectivas)
        ).filter(subComponente.id == subcomponente_id).first()
    asignaturasElectivas = subcomponete.asignaturasElectivas

    session.close()
    return asignaturasElectivas

def  obtener_asignaturasOB_componente(componente_id):
    session = Session()
    asiganturasOb = (
        session.query(Asignatura)
        .select_from(ComponenteObligactoria)
        .join(Componente, Componente.id == ComponenteObligactoria.componente_id)
        .filter(Componente.id == componente_id)
        .all()
    )

    session.close()
    return asiganturasOb

def  obtener_asignaturasEle_componente(componente_id):
    session = Session()
    
    asignaturas_electivas = (
        session.query(Asignatura)
        .select_from(ComponenteElectiva)
        .join(Componente, Componente.id == ComponenteElectiva.componente_id)
        .filter(Componente.id == componente_id)
        .all()
    )

    session.close()
    return asignaturas_electivas
