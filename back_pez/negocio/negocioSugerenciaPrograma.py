from sqlalchemy.orm import sessionmaker
from back_pez.db.model.asignatura import Asignatura
from back_pez.db.model.componente import Componente, ComponenteElectiva, ComponenteObligactoria, ComponenteSubComponente
from back_pez.db.model.perfilEstudiante import PerfilEstudiante
from back_pez.db.model.programa import Programa
from back_pez.db.model.subComponente import subComponente
from back_pez.db.model.usuario import Usuario
from negocio import negocioAvancePrograma
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

        programaUsuIds = [programa.id for programa in usuario.programa]
        minscsisinfo = 2 in programaUsuIds
        minscdistri = 4 in programaUsuIds

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
                if programa.id == 2 and minscdistri:
                    pass
                elif programa.id == 4 and minscsisinfo:
                    pass
                else:
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
        session.query(ComponenteObligactoria).options(
        selectinload(ComponenteObligactoria.asignaturasObligatorias))
        .filter(ComponenteObligactoria.componente_id == componente_id)
        .first()
    )

    if asiganturasOb:
        asignaturas = asiganturasOb.asignaturasObligatorias
    else:
        asignaturas = []
    session.close()
    return asignaturas

def  obtener_asignaturasEle_componente(componente_id):
    session = Session()
    
    compoElectiva = (
        session.query(ComponenteElectiva).options(
        selectinload(ComponenteElectiva.asignaturasElectivas)
        ).filter(ComponenteElectiva.componente_id == componente_id)
        .first()
    )

    if compoElectiva:
        asignaturas_electivas = compoElectiva.asignaturasElectivas
    else:
        asignaturas_electivas = []

    session.close()
    return asignaturas_electivas

def asignaturas_comun_programas(estudiante_id,id_programa):
    session = Session()
    estudiante = session.query(Usuario).options(
        selectinload(Usuario.programa)
        ).filter(Usuario.id == estudiante_id).first()
    
    programaComparar = session.query(Programa).filter(Programa.id == id_programa).first()
    session.close()
    
    asignaturasEstudiante = []
    asignaturaProgramaRecomendado = []

    for programa in estudiante.programa:
        asignaturasEstudiante.extend(obtener_asignaturas_requeridas_programa(programa.id))

    asignaturaProgramaRecomendado.extend(obtener_asignaturas_requeridas_programa(programaComparar.id))

    asignaturas_comunes = []
    
    for asignatura_estudiante in asignaturasEstudiante:
        for asignatura_recomendado in asignaturaProgramaRecomendado:
            if asignatura_estudiante.nombre == asignatura_recomendado.nombre and not(negocioAvancePrograma.ha_cursado_asignatura(estudiante.id,asignatura_recomendado.id)):
                asignaturas_comunes.append(asignatura_estudiante)
                print(asignatura_estudiante.nombre)

    return asignaturas_comunes
