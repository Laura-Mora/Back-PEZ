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

def generar_avance_estudiante(estudiante_id):
    # Obtener los programas en los que está inscrito el estudiante
    programas = obtener_programas_estudiante(estudiante_id)
    
    avance = {}
    
    for programa in programas:
        avance['programa'] = programa.nombre
        programa_id = programa.id
        avance['componentes'] = []
        
        # Obtener los componentes del programa
        componentes = obtener_componentes_programa(programa_id)
        asignaturas_vistas = set()
        
        for componente in componentes:
            componente_id = componente.id

            avance_componente = {}
            avance_componente['nombre'] = componente.nombre
            avance_componente['asignaturas'] = []
            avance_componente['subcomponentes'] = []
            
            creditos_requeridosCom = componente.cantCreditos  # Cantidad de créditos requeridos para el subcomponente
            creditos_vistosCom = 0 
            
            # Obtener los subcomponentes del componente
            subcomponentes = obtener_subcomponentes_componente(componente_id)

            for subcomponente in subcomponentes:
                subcomponente_id = subcomponente.id
                avance_subcomponente = {}
                avance_subcomponente['nombre'] = subcomponente.nombre
                avance_subcomponente['asignaturas'] = []
                
                creditos_requeridos = subcomponente.cantCreditos  # Cantidad de créditos requeridos para el subcomponente
                creditos_vistos = 0  # Variable para almacenar los créditos vistos por el estudiante
                
                for asignatura in obtener_asignaturasOB_subcomponente(subcomponente_id):
                    if asignatura.id not in asignaturas_vistas:

                        # Verificar si el estudiante ha cursado la asignatura
                        if ha_cursado_asignatura(estudiante_id, asignatura.id):
                            creditos_vistos += asignatura.creditos
                            asignaturas_vistas.add(asignatura.id)
                            # Agregar la asignatura al avance del estudiante
                            print(asignatura.nombre)
                            avance_subcomponente["asignaturas"].append(asignatura.nombre)
                        
                        if creditos_vistos >= creditos_requeridos:
                            break

                for asignatura in obtener_asignaturasEle_subcomponente(subcomponente_id):
                    if asignatura.id not in asignaturas_vistas:

                        # Verificar si el estudiante ha cursado la asignatura
                        if ha_cursado_asignatura(estudiante_id, asignatura.id):
                            creditos_vistos += asignatura.creditos
                            asignaturas_vistas.add(asignatura.id)
                            # Agregar la asignatura al avance del estudiante
                            print(asignatura.nombre)
                            avance_subcomponente["asignaturas"].append(asignatura.nombre)
                        
                        if creditos_vistos >= creditos_requeridos:
                            break
                
                avance_componente['subcomponentes'].append(avance_subcomponente)
            
            for asignatura in obtener_asignaturasOB_componente(componente_id):
                if asignatura.id not in asignaturas_vistas:

                    # Verificar si el estudiante ha cursado la asignatura
                    if ha_cursado_asignatura(estudiante_id, asignatura.id):
                        creditos_vistosCom += asignatura.creditos
                        asignaturas_vistas.add(asignatura.id)
                        # Agregar la asignatura al avance del estudiante
                        print(asignatura.nombre)
                        avance_componente["asignaturas"].append(asignatura.nombre)
                        
                    if creditos_vistosCom >= creditos_requeridosCom:
                        break

            for asignatura in obtener_asignaturasEle_componente(componente_id):
                if asignatura.id not in asignaturas_vistas:

                    # Verificar si el estudiante ha cursado la asignatura
                    if ha_cursado_asignatura(estudiante_id, asignatura.id):
                        creditos_vistosCom += asignatura.creditos
                        asignaturas_vistas.add(asignatura.id)
                        # Agregar la asignatura al avance del estudiante
                        print(asignatura.nombre)
                        avance_componente["asignaturas"].append(asignatura.nombre)
                        
                    if creditos_vistosCom >= creditos_requeridosCom:
                        break

            avance['componentes'].append(avance_componente)
    
    # Convertir el avance en JSON
    avance_json = json.dumps(avance, indent=4, ensure_ascii=False)
    
    return avance_json

def obtener_programas_estudiante(estudiante_id):

    session = Session()

    estudiante = session.query(Usuario).options(
        selectinload(Usuario.programa)).filter(Usuario.id == estudiante_id).first()
    programas = estudiante.programa

    session.close()

    return programas

def obtener_componentes_programa(programa_id):
    session = Session()
    programa = session.query(Programa).options(
        selectinload(Programa.componentes)).filter(Programa.id == programa_id).first()
    componentes = programa.componentes
    session.close()

    return componentes

def obtener_subcomponentes_componente(componente_id):
    session = Session()

    subcomponentes = (
        session.query(Componente)
        .select_from(ComponenteSubComponente)
        .join(Componente, Componente.id == ComponenteSubComponente.componente_id)
        .filter(Componente.id == componente_id)
        .all()
    )

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


def ha_cursado_asignatura(estudiante_id, asignatura_id):
    session = Session()

    estudiante = session.query(Usuario).options(
        selectinload(Usuario.perfilEstudiante)).filter(Usuario.id == estudiante_id).first()
    perfil = session.query(PerfilEstudiante).options(
        selectinload(PerfilEstudiante.asignaturasCursadas)).filter(PerfilEstudiante.id == estudiante.perfilEstudiante_id).first()

    asignaturas_cursadas= perfil.asignaturasCursadas

    esta = False
    for asignatura in asignaturas_cursadas:
        if asignatura.id == asignatura_id:
            esta = True

    session.close()

    return esta



