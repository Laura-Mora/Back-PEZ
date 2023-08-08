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
    
    avances = []

    for programa in programas:
        avance = {}
        avance['programa'] = programa.nombre
        programa_id = programa.id
        avance['componentes'] = []
        
       # Obtener los componentes del programa
        componentes = obtener_componentes_programa(programa_id)
        asignaturas_vistas = set()
        
        for componente in componentes:
            componente_id = componente.id

            avance_componente = {}  # Crear un nuevo diccionario para cada componente
            avance_componente['nombre'] = componente.nombre
            avance_componente['asignaturas'] = []
            avance_componente['subcomponentes'] = []
            
            creditos_requeridosCom = componente.cantCreditos  # Cantidad de créditos requeridos para el componente
            creditos_vistosCom = 0 
            
            asignaturas_contadasCom = 0
            
            # Obtener los subcomponentes del componente
            subcomponentes = obtener_subcomponentes_componente(componente_id)

            for subcomponente in subcomponentes:
                subcomponente_id = subcomponente.id
                avance_subcomponente = {}
                avance_subcomponente['nombre'] = subcomponente.nombre
                avance_subcomponente['asignaturas'] = []
                
                print(subcomponente.nombre)
                creditos_vistos = 0  # Variable para almacenar los créditos vistos por el estudiante
                asignaturas_contadas = 0

                if subcomponente.cantCreditos is not None:
                    creditos_requeridos = subcomponente.cantCreditos
                    # Resto del código para procesar el subcomponente con cantCreditos
                else:
                    creditos_requeridos = -1

                if subcomponente.cantAsignaturas is not None:
                    asignaturas_minimas = subcomponente.cantAsignaturas
                else:
                    asignaturas_minimas = 0
                
                for asignatura in obtener_asignaturasOB_subcomponente(subcomponente_id):
                    if asignatura.id not in asignaturas_vistas:
                        # Verificar si el estudiante ha cursado la asignatura
                        if ha_cursado_asignatura(estudiante_id, asignatura.id):
                            creditos_vistos += asignatura.creditos
                            asignaturas_vistas.add(asignatura.id)
                            # Agregar la asignatura al avance del estudiante
                            avance_subcomponente["asignaturas"].append(asignatura.nombre)
                            asignaturas_contadas += 1
                        
                        if creditos_vistos >= creditos_requeridos and creditos_requeridos > -1:
                            break

                for asignatura in obtener_asignaturasEle_subcomponente(subcomponente_id):
                    if asignatura.id not in asignaturas_vistas:
                        # Verificar si el estudiante ha cursado la asignatura
                        if ha_cursado_asignatura(estudiante_id, asignatura.id):
                            creditos_vistos += asignatura.creditos
                            asignaturas_vistas.add(asignatura.id)
                            # Agregar la asignatura al avance del estudiante
                            avance_subcomponente["asignaturas"].append(asignatura.nombre)
                            asignaturas_contadas += 1
                        
                        if creditos_vistos >= creditos_requeridos and creditos_requeridos > -1:
                            break
                
                avance_componente['subcomponentes'].append(avance_subcomponente)
                
                # Verificar si se ha alcanzado la cantidad mínima de asignaturas por subcomponente
                if asignaturas_contadas >= asignaturas_minimas:
                    asignaturas_contadasCom += 1
            
            asiganturasCompoOB = obtener_asignaturasOB_componente(componente_id)
            for asignatura in asiganturasCompoOB:
                if asignatura.id not in asignaturas_vistas:
                    # Verificar si el estudiante ha cursado la asignatura
                    if ha_cursado_asignatura(estudiante_id, asignatura.id):
                        creditos_vistosCom += asignatura.creditos
                        asignaturas_vistas.add(asignatura.id)
                        # Agregar la asignatura al avance del estudiante
                        avance_componente["asignaturas"].append(asignatura.nombre)
                        asignaturas_contadasCom += 1
                        
                    if creditos_vistosCom >= creditos_requeridosCom:
                        break
            
            asignaturasCompoEle = obtener_asignaturasEle_componente(componente_id)
            for asignatura in asignaturasCompoEle:
                if asignatura.id not in asignaturas_vistas:
                    # Verificar si el estudiante ha cursado la asignatura
                    if ha_cursado_asignatura(estudiante_id, asignatura.id):
                        creditos_vistosCom += asignatura.creditos
                        asignaturas_vistas.add(asignatura.id)
                        # Agregar la asignatura al avance del estudiante
                        avance_componente["asignaturas"].append(asignatura.nombre)
                        asignaturas_contadasCom += 1
                        
                    if creditos_vistosCom >= creditos_requeridosCom:
                        break


            avance['componentes'].append(avance_componente)

        avances.append(avance)
    
    # Convertir el avance en JSON
    avance_json = json.dumps(avances, indent=4, ensure_ascii=False)
    
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

def faltaParacompletarProgramas(estudiante_id):
     # Obtener los programas en los que está inscrito el estudiante
    programas = obtener_programas_estudiante(estudiante_id)
    
    avances = []

    for programa in programas:
        avance = {}
        avance['programa'] = programa.nombre
        programa_id = programa.id
        avance['componentes'] = []
        
       # Obtener los componentes del programa
        componentes = obtener_componentes_programa(programa_id)
        asignaturas_vistas = set()
        
        for componente in componentes:
            componente_id = componente.id

            avance_componente = {}  # Crear un nuevo diccionario para cada componente
            avance_componente['nombre'] = componente.nombre
            avance_componente['asignaturas'] = []
            avance_componente['subcomponentes'] = []
            
            creditos_requeridosCom = componente.cantCreditos  # Cantidad de créditos requeridos para el componente
            creditos_vistosCom = 0 
            
            asignaturas_contadasCom = 0
            
            # Obtener los subcomponentes del componente
            subcomponentes = obtener_subcomponentes_componente(componente_id)

            for subcomponente in subcomponentes:
                subcomponente_id = subcomponente.id
                avance_subcomponente = {}
                avance_subcomponente['nombre'] = subcomponente.nombre
                avance_subcomponente['asignaturas'] = []
                
                print(subcomponente.nombre)
                creditos_vistos = 0  # Variable para almacenar los créditos vistos por el estudiante
                asignaturas_contadas = 0

                if subcomponente.cantCreditos is not None:
                    creditos_requeridos = subcomponente.cantCreditos
                    # Resto del código para procesar el subcomponente con cantCreditos
                else:
                    creditos_requeridos = -1

                if subcomponente.cantAsignaturas is not None:
                    asignaturas_minimas = subcomponente.cantAsignaturas
                else:
                    asignaturas_minimas = 0
                
                for asignatura in obtener_asignaturasOB_subcomponente(subcomponente_id):
                    if asignatura.id not in asignaturas_vistas:
                        # Verificar si el estudiante ha cursado la asignatura
                        if ha_cursado_asignatura(estudiante_id, asignatura.id):
                            creditos_vistos += asignatura.creditos
                            asignaturas_contadas += 1
                        
                        if creditos_vistos >= creditos_requeridos and creditos_requeridos > -1:
                            break

                for asignatura in obtener_asignaturasEle_subcomponente(subcomponente_id):
                    if asignatura.id not in asignaturas_vistas:
                        # Verificar si el estudiante ha cursado la asignatura
                        if ha_cursado_asignatura(estudiante_id, asignatura.id):
                            creditos_vistos += asignatura.creditos
                            asignaturas_contadas += 1
                        
                        if creditos_vistos >= creditos_requeridos and creditos_requeridos > -1:
                            break

                if creditos_vistos < creditos_requeridos:
                    #Calcular asignaturas subcomponente
                    for asignatura in obtener_asignaturasOB_subcomponente(subcomponente_id):
                        if asignatura.id not in asignaturas_vistas:
                            # Verificar si el estudiante ha cursado la asignatura
                            if not ha_cursado_asignatura(estudiante_id, asignatura.id):
                                asignaturas_vistas.add(asignatura.id)
                                # Agregar la asignatura al avance del estudiante
                                avance_subcomponente["asignaturas"].append(asignatura.nombre)

                    for asignatura in obtener_asignaturasEle_subcomponente(subcomponente_id):
                        if asignatura.id not in asignaturas_vistas:
                            # Verificar si el estudiante ha cursado la asignatura
                            if not ha_cursado_asignatura(estudiante_id, asignatura.id):
                                asignaturas_vistas.add(asignatura.id)
                                # Agregar la asignatura al avance del estudiante
                                avance_subcomponente["asignaturas"].append(asignatura.nombre)
                                
                
                avance_componente['subcomponentes'].append(avance_subcomponente)
                
                # Verificar si se ha alcanzado la cantidad mínima de asignaturas por subcomponente
                if asignaturas_contadas >= asignaturas_minimas:
                    asignaturas_contadasCom += 1
            
            asiganturasCompoOB = obtener_asignaturasOB_componente(componente_id)
            for asignatura in asiganturasCompoOB:
                if asignatura.id not in asignaturas_vistas:
                    # Verificar si el estudiante ha cursado la asignatura
                    if ha_cursado_asignatura(estudiante_id, asignatura.id):
                        creditos_vistosCom += asignatura.creditos
                        asignaturas_contadasCom += 1
                        
                    if creditos_vistosCom >= creditos_requeridosCom:
                        break
            
            asignaturasCompoEle = obtener_asignaturasEle_componente(componente_id)
            for asignatura in asignaturasCompoEle:
                if asignatura.id not in asignaturas_vistas:
                    # Verificar si el estudiante ha cursado la asignatura
                    if ha_cursado_asignatura(estudiante_id, asignatura.id):
                        creditos_vistosCom += asignatura.creditos
                        asignaturas_contadasCom += 1
                        
                    if creditos_vistosCom >= creditos_requeridosCom:
                        break

            if creditos_vistosCom < creditos_requeridosCom:
                for asignatura in asiganturasCompoOB:
                    if asignatura.id not in asignaturas_vistas:
                        # Verificar si el estudiante ha cursado la asignatura
                        if not ha_cursado_asignatura(estudiante_id, asignatura.id):
                            asignaturas_vistas.add(asignatura.id)
                            # Agregar la asignatura al avance del estudiante
                            avance_componente["asignaturas"].append(asignatura.nombre)

                
                asignaturasCompoEle = obtener_asignaturasEle_componente(componente_id)
                for asignatura in asignaturasCompoEle:
                    if asignatura.id not in asignaturas_vistas:
                        # Verificar si el estudiante ha cursado la asignatura
                        if not ha_cursado_asignatura(estudiante_id, asignatura.id):
                            asignaturas_vistas.add(asignatura.id)
                            # Agregar la asignatura al avance del estudiante
                            avance_componente["asignaturas"].append(asignatura.nombre)
                            
                        if creditos_vistosCom >= creditos_requeridosCom:
                            break


            avance['componentes'].append(avance_componente)

        avances.append(avance)
            # Convertir el avance en JSON
    avance_json = json.dumps(avances, indent=4, ensure_ascii=False)
    
    return avance_json


