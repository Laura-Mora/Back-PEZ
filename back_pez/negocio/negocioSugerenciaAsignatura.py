from typing import List, Set
from db.dbconfig import engine
from sqlalchemy import exists
from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import selectinload

from back_pez.db.model.perfilEstudiante import PerfilEstudiante
from back_pez.db.model.asignatura import Asignatura

Session = sessionmaker(bind=engine)

# Función para recomendar asignaturas al estudiante
def recomendar_asignaturas(id:int):
    session = Session()

    asignaturas_recomendadas = set()

    estudiante = session.query(PerfilEstudiante).options(
        selectinload(PerfilEstudiante.asignaturasCursadas),
        selectinload(PerfilEstudiante.actividadesGusto),
        selectinload(PerfilEstudiante.competenciasGusto),
        selectinload(PerfilEstudiante.horariosPreferencias),
        selectinload(PerfilEstudiante.tematicasGusto),
        selectinload(PerfilEstudiante.modalidadPreferencia),
        selectinload(PerfilEstudiante.modoEnsenianzaPreferencia)
        ).filter(PerfilEstudiante.id == id).first()
    
    asignaturas_disponibles = session.query(Asignatura).options(
    selectinload(Asignatura.modalidad),
    selectinload(Asignatura.modoEnsenianza),
    selectinload(Asignatura.profesores),
    selectinload(Asignatura.horarios),
    selectinload(Asignatura.competencias),
    selectinload(Asignatura.actividades),
    selectinload(Asignatura.tematicas)
    ).all()

    # Creamos diccionarios que mapean horarios y actividades a las asignaturas
    horarios_asignaturas = {}
    actividades_asignaturas = {}

    for asignatura in asignaturas_disponibles:
        for horario in asignatura.horarios:
            if horario.id not in horarios_asignaturas:
                horarios_asignaturas[horario.id] = set()
            horarios_asignaturas[horario.id].add(asignatura.id)

    for actividad in asignatura.actividades:
        if actividad.id not in actividades_asignaturas:
            actividades_asignaturas[actividad.id] = set()
        actividades_asignaturas[actividad.id].add(asignatura.id)

    # Creamos diccionarios que mapean temáticas y competencias a las asignaturas
    tematicas_asignaturas = {}
    competencias_asignaturas = {}

    for asignatura in asignaturas_disponibles:
        for tematica in asignatura.tematicas:
            if tematica.id not in tematicas_asignaturas:
                tematicas_asignaturas[tematica.id] = set()
            tematicas_asignaturas[tematica.id].add(asignatura.id)

    for competencia in asignatura.competencias:
        if competencia.id not in competencias_asignaturas:
            competencias_asignaturas[competencia.id] = set()
        competencias_asignaturas[competencia.id].add(asignatura.id)

    asignaturas_recomendadas = set()

    # Obtener la lista de asignaturas que ya ha cursado el estudiante
    asignaturas_cursadas = set(estudiante.asignaturasCursadas)

    # Obtener las preferencias del estudiante en forma de conjuntos
    competencias_gustadas = {competencia.id for competencia in estudiante.competenciasGusto}
    tematicas_gustadas = {tematica.id for tematica in estudiante.tematicasGusto}
    
    # Filtrar asignaturas disponibles según las preferencias del estudiante
    asignaturas_temporales = set()
    for asignatura in asignaturas_disponibles:
        # Verificar si las temáticas y competencias están presentes en la asignatura
        if tematicas_gustadas.intersection(tematicas_asignaturas.get(asignatura.id, set())) and \
           competencias_gustadas.intersection(competencias_asignaturas.get(asignatura.id, set())):
            print(asignatura.id)
            asignaturas_recomendadas.add(asignatura)
        elif competencias_gustadas.intersection(competencias_asignaturas.get(asignatura.id, set())):
            print(asignatura.id)
            asignaturas_temporales.add(asignatura)
        elif tematicas_gustadas.intersection(tematicas_asignaturas.get(asignatura.id, set())):
            print(asignatura.id)
            asignaturas_temporales.add(asignatura)

    # Si no se encontraron asignaturas que cumplan con las temáticas y competencias, añadir asignaturas por competencias
    if not asignaturas_recomendadas:
        asignaturas_recomendadas.update(asignaturas_temporales)

    # Filtrar asignaturas que el estudiante ya cursó
    asignaturas_recomendadas -= asignaturas_cursadas

    return asignaturas_recomendadas


def sugerir_asignaturas_por_preferencias(id: int):
    session = Session()

    asignaturas_recomendadas = set()

    estudiante = session.query(PerfilEstudiante).options(
        selectinload(PerfilEstudiante.asignaturasCursadas),
        selectinload(PerfilEstudiante.actividadesGusto),
        selectinload(PerfilEstudiante.competenciasGusto),
        selectinload(PerfilEstudiante.horariosPreferencias),
        selectinload(PerfilEstudiante.tematicasGusto),
        selectinload(PerfilEstudiante.modalidadPreferencia),
        selectinload(PerfilEstudiante.modoEnsenianzaPreferencia)
        ).filter(PerfilEstudiante.id == id).first()
    
    asignaturas = session.query(Asignatura).options(
    selectinload(Asignatura.modalidad),
    selectinload(Asignatura.modoEnsenianza),
    selectinload(Asignatura.profesores),
    selectinload(Asignatura.horarios),
    selectinload(Asignatura.competencias),
    selectinload(Asignatura.actividades),
    selectinload(Asignatura.tematicas)
    ).all()

    modalidades_preferidas = {modalidad.id for modalidad in estudiante.modalidadPreferencia}
    modos_ensenianza_preferidos = {modo.id for modo in estudiante.modoEnsenianzaPreferencia}
    actividades_gustadas = {actividad.id for actividad in estudiante.actividadesGusto}

    asignaturas_cursadas = set(estudiante.asignaturasCursadas)

    for asignatura in asignaturas:

        if (not modalidades_preferidas or asignatura.modalidad.id in modalidades_preferidas) and \
           (not modos_ensenianza_preferidos or asignatura.modoEnsenianza.id in modos_ensenianza_preferidos) and \
           (not actividades_gustadas or any(actividad.id in actividades_gustadas for actividad in asignatura.actividades)):
            print(asignatura.id)
            asignaturas_recomendadas.add(asignatura)

    asignaturas_recomendadas -= asignaturas_cursadas

    return asignaturas_recomendadas



