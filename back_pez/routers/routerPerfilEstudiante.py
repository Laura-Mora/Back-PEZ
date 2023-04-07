from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import sessionmaker
from db.model.perfilEstudiante import PerfilEstudiante
from back_pez.db.model.actividad import Actividad, ActividadModelo
from back_pez.db.model.asignatura import Asignatura, AsignaturaModelo
from back_pez.db.model.competencia import Competencia, CompetenciaModel
from back_pez.db.model.componenteClase import ComponenteClase, ComponenteClaseModelo
from back_pez.db.model.contenido import Contenido, ContenidoModelo
from back_pez.db.model.horario import Horario, HorarioModel
from back_pez.db.model.modoEnsenianza import ModoEnsenianza, ModoEnsenianzaModel

from db.dbconfig import engine

router = APIRouter(prefix="/perfilEstudiante",
                   tags=["perfilEstudiante"],
                   responses={404: {"message": "No encontrado"}})

Session = sessionmaker(bind=engine)

@router.get("/")
def perfilesEstudiante():
    session = Session()
    perfiles = session.query(PerfilEstudiante).all()
    session.close()
    return perfiles

@router.get("/{id}")  # Path
def perfilEstudiante(id: str):
    session = Session()
    perfil = session.query(PerfilEstudiante).filter(PerfilEstudiante.id == id).first()
    session.close()
    if not perfil:
        raise HTTPException(status_code=404, detail='PerfilEstudiante no encontrado')
    return perfil


@router.post('/')
def crear_perfil(id: int, profesion: str, javeriano: bool, semestre: int, areaDesempenio: str,
    asignaturasCursadas: List[AsignaturaModelo], asignaturasGustadas: List[AsignaturaModelo],
    modalidadPreferencia:List[ComponenteClaseModelo],modoEnsenianzaPreferencia: List[ModoEnsenianzaModel],
    horariosPreferencias: List[HorarioModel], competenciasGusto: List[CompetenciaModel],actividadesGusto: List[ActividadModelo],
    tematicasGusto: List[ContenidoModelo]):
    session = Session()
    nuevo_perfil = PerfilEstudiante(id=id,profesion=profesion, javeriano=javeriano, semestre=semestre, areaDesempenio=areaDesempenio,
    asignaturasCursadas=asignaturasCursadas, asignaturasGustadas=asignaturasGustadas,
    modalidadPreferencia=modalidadPreferencia,modoEnsenianzaPreferencia=modoEnsenianzaPreferencia,
    horariosPreferencias=horariosPreferencias, competenciasGusto=competenciasGusto,actividadesGusto=actividadesGusto,
    tematicasGusto=tematicasGusto)
    session.add(nuevo_perfil)
    session.commit()
    session.close()
    return nuevo_perfil

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