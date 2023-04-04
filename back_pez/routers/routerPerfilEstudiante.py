from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import sessionmaker
from db.model.perfilEstudiante import PerfilEstudiante
from back_pez.db.model.actividad import Actividad
from back_pez.db.model.asignatura import Asignatura
from back_pez.db.model.competencia import Competencia
from back_pez.db.model.componenteClase import ComponenteClase
from back_pez.db.model.contenido import Contenido
from back_pez.db.model.horario import Horario
from back_pez.db.model.modoEnsenianza import ModoEnsenianza

from db.dbconfig import engine

router = APIRouter(prefix="/perfilEstudiante",
                   tags=["perfilEstudiante"],
                   responses={404: {"message": "No encontrado"}})

Session = sessionmaker(bind=engine)

@router.get("/")
async def perfilesEstudiante():
    session = Session()
    perfiles = session.query(PerfilEstudiante).all()
    session.close()
    return perfiles

@router.get("/{id}")  # Path
async def perfilEstudiante(id: str):
    session = Session()
    perfil = session.query(PerfilEstudiante).filter(PerfilEstudiante.id == id).first()
    session.close()
    if not perfil:
        raise HTTPException(status_code=404, detail='PerfilEstudiante no encontrado')
    return perfil


@router.post('/')
async def crear_perfil(id: int, profesion: str, javeriano: bool, semestre: int, areaDesempenio: str,
    asignaturasCursadas: List[Asignatura], asignaturasGustadas: List[Asignatura],
    modalidadPreferencia:List[ComponenteClase],modoEnsenianzaPreferencia: List[ModoEnsenianza],
    horariosPreferencias: List[Horario], competenciasGusto: List[Competencia],actividadesGusto: List[Actividad],
    tematicasGusto: List[Contenido]):
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