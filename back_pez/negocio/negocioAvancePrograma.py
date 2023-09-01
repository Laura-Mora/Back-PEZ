from sqlalchemy.orm import sessionmaker
from back_pez.db.model.asignatura import Asignatura
from back_pez.db.model.componente import Componente, ComponenteElectiva, ComponenteObligactoria, ComponenteSubComponente
from back_pez.db.model.perfilEstudiante import PerfilEstudiante
from back_pez.db.model.programa import Programa
from back_pez.db.model.subComponente import subComponente
from back_pez.db.model.usuario import Usuario
from negocio import negocioSugerenciaPrograma
from db.dbconfig import engine
from sqlalchemy import exists

from sqlalchemy.orm import selectinload

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from io import BytesIO

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

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
            avance_componente['cantCreditos'] = 0
            avance_componente['creditosVistos'] = 0
            
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
                avance_subcomponente['cantCreditos'] = 0
                avance_subcomponente['creditosVistos'] = 0
                avance_subcomponente['asignaturas_minimas'] = 0
                
                print(subcomponente.nombre)
                creditos_vistos = 0  # Variable para almacenar los créditos vistos por el estudiante
                asignaturas_contadas = 0

                if subcomponente.cantCreditos is not None:
                    creditos_requeridos = subcomponente.cantCreditos
                    avance_subcomponente['cantCreditos'] = creditos_requeridos
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
                
                avance_subcomponente['creditosVistos'] = creditos_vistos
                avance_subcomponente['asignaturas_minimas'] = asignaturas_minimas
                
                avance_componente['subcomponentes'].append(avance_subcomponente)
                creditos_vistosCom += creditos_vistos
                
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
            
            avance_componente['cantCreditos'] = creditos_requeridosCom
            avance_componente['creditosVistos'] = creditos_vistosCom

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
            avance_componente['cantCreditos'] = 0
            avance_componente['creditosVistos'] = 0
            
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
                avance_subcomponente['creditosVistos'] = 0
                avance_subcomponente['asignaturas_minimas'] = 0
                
                print(subcomponente.nombre)
                creditos_vistos = 0  # Variable para almacenar los créditos vistos por el estudiante
                asignaturas_contadas = 0

                if subcomponente.cantCreditos is not None:
                    creditos_requeridos = subcomponente.cantCreditos
                    avance_subcomponente['cantCreditos'] = creditos_requeridos
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
                            asignaturas_vistas.add(asignatura.id)

                        if creditos_vistos >= creditos_requeridos and creditos_requeridos > -1:
                            break

                for asignatura in obtener_asignaturasEle_subcomponente(subcomponente_id):
                    if asignatura.id not in asignaturas_vistas:
                        # Verificar si el estudiante ha cursado la asignatura
                        if ha_cursado_asignatura(estudiante_id, asignatura.id):
                            creditos_vistos += asignatura.creditos
                            asignaturas_contadas += 1
                            asignaturas_vistas.add(asignatura.id)
                        
                        if creditos_vistos >= creditos_requeridos and creditos_requeridos > -1:
                            break

                if creditos_vistos < creditos_requeridos:
                    #Calcular asignaturas subcomponente
                    for asignatura in obtener_asignaturasOB_subcomponente(subcomponente_id):
                        if asignatura.id not in asignaturas_vistas:
                            # Verificar si el estudiante ha cursado la asignatura
                            if not ha_cursado_asignatura(estudiante_id, asignatura.id):

                                # Agregar la asignatura al avance del estudiante
                                avance_subcomponente["asignaturas"].append(asignatura.nombre)

                    for asignatura in obtener_asignaturasEle_subcomponente(subcomponente_id):
                        if asignatura.id not in asignaturas_vistas:
                            # Verificar si el estudiante ha cursado la asignatura
                            if not ha_cursado_asignatura(estudiante_id, asignatura.id):

                                # Agregar la asignatura al avance del estudiante
                                avance_subcomponente["asignaturas"].append(asignatura.nombre)

                avance_subcomponente['creditosVistos'] = creditos_vistos
                avance_subcomponente['asignaturas_minimas'] = asignaturas_minimas                
                
                avance_componente['subcomponentes'].append(avance_subcomponente)
                creditos_vistosCom += creditos_vistos
                
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
                        asignaturas_vistas.add(asignatura.id)
                        
                    if creditos_vistosCom >= creditos_requeridosCom:
                        break
            
            asignaturasCompoEle = obtener_asignaturasEle_componente(componente_id)
            for asignatura in asignaturasCompoEle:
                if asignatura.id not in asignaturas_vistas:
                    # Verificar si el estudiante ha cursado la asignatura
                    if ha_cursado_asignatura(estudiante_id, asignatura.id):
                        creditos_vistosCom += asignatura.creditos
                        asignaturas_contadasCom += 1
                        asignaturas_vistas.add(asignatura.id)
                        
                    if creditos_vistosCom >= creditos_requeridosCom:
                        break

            if creditos_vistosCom < creditos_requeridosCom:
                for asignatura in asiganturasCompoOB:
                    if asignatura.id not in asignaturas_vistas:
                        # Verificar si el estudiante ha cursado la asignatura
                        if not ha_cursado_asignatura(estudiante_id, asignatura.id):
                            # Agregar la asignatura al avance del estudiante
                            avance_componente["asignaturas"].append(asignatura.nombre)

                
                asignaturasCompoEle = obtener_asignaturasEle_componente(componente_id)
                for asignatura in asignaturasCompoEle:
                    if asignatura.id not in asignaturas_vistas:
                        # Verificar si el estudiante ha cursado la asignatura
                        if not ha_cursado_asignatura(estudiante_id, asignatura.id):
                            # Agregar la asignatura al avance del estudiante
                            avance_componente["asignaturas"].append(asignatura.nombre)
                            

            avance_componente['cantCreditos'] = creditos_requeridosCom
            avance_componente['creditosVistos'] = creditos_vistosCom

            avance['componentes'].append(avance_componente)

        avances.append(avance)
            # Convertir el avance en JSON
    avance_json = json.dumps(avances, indent=4, ensure_ascii=False)
    
    return avance_json


def avance_programa_recomendado(id_programa,estudiante_id):

    session = Session()

    programa = session.query(Programa).filter(Programa.id == id_programa).first()


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
        avance_componente['cantCreditos'] = 0
        avance_componente['creditosVistos'] = 0
            
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
            avance_subcomponente['creditosVistos'] = 0
            avance_subcomponente['asignaturas_minimas'] = 0
                
            print(subcomponente.nombre)
            creditos_vistos = 0  # Variable para almacenar los créditos vistos por el estudiante
            asignaturas_contadas = 0

            if subcomponente.cantCreditos is not None:
                creditos_requeridos = subcomponente.cantCreditos
                avance_subcomponente['cantCreditos'] = creditos_requeridos
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

            avance_subcomponente['creditosVistos'] = creditos_vistos
            avance_subcomponente['asignaturas_minimas'] = asignaturas_minimas  
              
            avance_componente['subcomponentes'].append(avance_subcomponente)
            creditos_vistosCom += creditos_vistos
                
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

        avance_componente['cantCreditos'] = creditos_requeridosCom
        avance_componente['creditosVistos'] = creditos_vistosCom

        avance['componentes'].append(avance_componente)

    
    session.close()
    # Convertir el avance en JSON
    avance_json = json.dumps(avance, indent=4, ensure_ascii=False)
    
    return avance_json


def generar_pdf_avance_programa(estudiante_id):

    session = Session()

    estudiante = session.query(Usuario).options(
        selectinload(Usuario.programa)).filter(Usuario.id == estudiante_id).first()
    
    correo = estudiante.correo
    
    session.close()

    avance_json = generar_avance_estudiante(estudiante_id)
    avance_programa = json.loads(avance_json)
    reporteFalta_json = faltaParacompletarProgramas(estudiante_id)
    reporteFalta = json.loads(reporteFalta_json)

    doc = SimpleDocTemplate("avance_programa.pdf", pagesize=letter)
    story = []

    # Estilo de párrafo para las viñetas
    styles = getSampleStyleSheet()
    estilo_bullet = styles["Bullet"]
    
    for programa in avance_programa:
        texto_programa = f"Para el programa {programa['programa']}, este es tu avance hasta ahora"
        pp = Paragraph(texto_programa)
        story.append(pp)
        story.append(Spacer(1, 12))
        for componente in programa['componentes']:
            texto_componente = f"Para el componente {componente['nombre']}, haz cursado {componente['creditosVistos']} créditos de {componente['cantCreditos']} créditos."
            cp = Paragraph(texto_componente)
            story.append(cp)
            story.append(Spacer(1, 12))
            for asignatura_info in componente['asignaturas']:
                texto_asignatura = f"• {asignatura_info}"
                p = Paragraph(texto_asignatura, estilo_bullet)
                story.append(p)
                story.append(Spacer(1, 12))
            for subcomponente in componente['subcomponentes']:
                texto_subcomponente = f"Para el subcomponente {subcomponente['nombre']}, haz cursado {subcomponente['creditosVistos']} créditos de {subcomponente['cantCreditos']} créditos."
                sp = Paragraph(texto_subcomponente)
                story.append(sp)
                story.append(Spacer(1, 12))
                for asignatura_info in subcomponente['asignaturas']:
                    texto_asignatura = f"• {asignatura_info}"
                    p = Paragraph(texto_asignatura, estilo_bullet)
                    story.append(p)
                    story.append(Spacer(1, 12))

    for programa in reporteFalta:
        texto_programa = f"Para el programa {programa['programa']}, puedes cursar para cumplir los requisitos"
        pp = Paragraph(texto_programa)
        story.append(pp)
        story.append(Spacer(1, 12))
        for componente in programa['componentes']:
            texto_componente = f"Para el componente {componente['nombre']}, haz cursado {componente['creditosVistos']} créditos de {componente['cantCreditos']} créditos. Para cursar los créditos que te hacen falta puedes ver:"
            cp = Paragraph(texto_componente)
            story.append(cp)
            story.append(Spacer(1, 12))
            for asignatura_info in componente['asignaturas']:
                # Crear un párrafo con viñetas para cada asignatura
                texto_asignatura = f"• {asignatura_info}"
                p = Paragraph(texto_asignatura, estilo_bullet)
                story.append(p)
                story.append(Spacer(1, 12))
            for subcomponente in componente['subcomponentes']:
                texto_subcomponente = f"Para el subcomponente {subcomponente['nombre']}, haz cursado {subcomponente['creditosVistos']} créditos de {subcomponente.cantCreditos} créditos. Para cursar los créditos que te hacen falta puedes ver:"
                sp = Paragraph(texto_subcomponente)
                story.append(sp)
                story.append(Spacer(1, 12))
                for asignatura_info in subcomponente['asignaturas']:
                    # Crear un párrafo con viñetas para cada asignatura
                    texto_asignatura = f"• {asignatura_info}"
                    p = Paragraph(texto_asignatura, estilo_bullet)
                    story.append(p)
                    story.append(Spacer(1, 12))
    # Crear el documento PDF en memoria
    buffer = BytesIO()
    doc.build(story, canvasmaker=canvas.Canvas)

    enviar_correo_avance("avance_programa.pdf", correo)

    return buffer

def enviar_correo_avance(archivo_adjunto, correo):
    # Datos de configuración del correo
    remitente = 'lalis.mora98@gmail.com'
    contraseña = 'wtksfmxjegqagtpx'
    servidor_smtp = 'smtp.gmail.com'
    puerto = 587

    destinatario = correo
    #destinatario ='lalis.mora98@gmail.com'
    asunto = 'Avance programa'
    mensaje = 'Buenos días, adjunto el avance del programa.'

    # Crear objeto MIME para el correo
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto

    # Agregar cuerpo del mensaje
    msg.attach(MIMEText(mensaje, 'plain'))

    # Agregar archivo adjunto
    with open(archivo_adjunto, "rb") as adjunto:
        part = MIMEApplication(adjunto.read(), Name=archivo_adjunto)
        part['Content-Disposition'] = f'attachment; filename="{archivo_adjunto}"'
        msg.attach(part)

    # Establecer conexión con el servidor SMTP
    server = smtplib.SMTP(host=servidor_smtp, port=puerto)
    server.starttls()
    server.login(remitente, contraseña)

    # Enviar correo
    server.sendmail(remitente, destinatario, msg.as_string())
    server.quit()

def generar_pdf_programa_suge(estudiante_id,id_programa):
    session = Session()

    estudiante = session.query(Usuario).options(
        selectinload(Usuario.programa)).filter(Usuario.id == estudiante_id).first()
    
    correo = estudiante.correo
    
    session.close()

    avance_json = avance_programa_recomendado(id_programa,estudiante_id)
    avance_programa = json.loads(avance_json)

    asignaturasComun = negocioSugerenciaPrograma.asignaturas_comun_programas(estudiante_id,id_programa)

    doc = SimpleDocTemplate("avance_programa_sugerido.pdf", pagesize=letter)
    story = []

    # Estilo de párrafo para las viñetas
    styles = getSampleStyleSheet()
    estilo_bullet = styles["Bullet"]  

    texto_programa = f"Para el programa {avance_programa['programa']}, este es tu avance hasta ahora"
    pp = Paragraph(texto_programa)
    story.append(pp)
    story.append(Spacer(1, 12))
    for componente in avance_programa['componentes']:
        texto_componente = f"Para el componente {componente['nombre']}, haz cursado {componente['creditosVistos']} créditos de {componente['cantCreditos']} créditos."
        cp = Paragraph(texto_componente)
        story.append(cp)
        story.append(Spacer(1, 12))
        for asignatura_info in componente['asignaturas']:
            texto_asignatura = f"• {asignatura_info}"
            p = Paragraph(texto_asignatura, estilo_bullet)
            story.append(p)
            story.append(Spacer(1, 12))
        for subcomponente in componente['subcomponentes']:
            texto_subcomponente = f"Para el subcomponente {subcomponente['nombre']}, haz cursado {subcomponente['creditosVistos']} créditos de {subcomponente['cantCreditos']} créditos."
            sp = Paragraph(texto_subcomponente)
            story.append(sp)
            story.append(Spacer(1, 12))
            for asignatura_info in subcomponente['asignaturas']:
                texto_asignatura = f"• {asignatura_info}"
                p = Paragraph(texto_asignatura, estilo_bullet)
                story.append(p)
                story.append(Spacer(1, 12))

    texto_asignaturaComun = f"Puedes cursar algunas de las siguientes asignaturas y te sirven para el programa que estas cursando y el sugerido"
    acp = Paragraph(texto_asignaturaComun)
    story.append(acp)
    story.append(Spacer(1, 12))

    for asignatura in asignaturasComun:
        texto_asignatura = f" • {asignatura.nombre}"
        ap = Paragraph(texto_asignatura)
        story.append(ap)
        story.append(Spacer(1, 12))

    # Crear el documento PDF en memoria
    buffer = BytesIO()
    doc.build(story, canvasmaker=canvas.Canvas)

    enviar_correo_avance("avance_programa_sugerido.pdf", correo)

    return buffer