from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import insert
from sqlalchemy import inspect
from back_pez.db.model.actividad import Actividad
from back_pez.db.model.asignatura import Asignatura
from back_pez.db.model.base import Base
from back_pez.db.model.componente import Componente
from back_pez.db.model.componenteClase import ComponenteClase
from back_pez.db.model.reseniaAsignatura import ReseniaAsignatura
from back_pez.db.model.tematica import Tematica
from back_pez.db.model.horario import Horario
from back_pez.db.model.modoEnsenianza import ModoEnsenianza
from back_pez.db.model.competencia import Competencia
from back_pez.db.model.perfilEstudiante import PerfilEstudiante
from back_pez.db.model.profesor import Profesor
from back_pez.db.model.programa import Programa
from back_pez.db.model.subComponente import subComponente
from back_pez.db.model.usuario import Usuario
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("postgresql+psycopg2://PEZ:PEZPassword@localhost:5432/PEZDB")
Base.metadata.create_all(engine)

borrarTablas = False

def table_exists(name):
    if borrarTablas:
        try:
            name.__table__.drop(engine)
        except:
            pass

table_exists(Profesor)
table_exists(Competencia)
table_exists(Tematica)
table_exists(ModoEnsenianza)
table_exists(ComponenteClase)
table_exists(Horario)
table_exists(Actividad)
table_exists(Asignatura)
table_exists(subComponente)
table_exists(Componente)
table_exists(PerfilEstudiante)
table_exists(Programa)
table_exists(Usuario)
table_exists(ReseniaAsignatura)