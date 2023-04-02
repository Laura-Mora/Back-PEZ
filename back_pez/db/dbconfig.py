from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import insert
from back_pez.db.model.actividad import Actividad
from back_pez.db.model.asignatura import Asignatura
from back_pez.db.model.componente import Componente
from back_pez.db.model.componenteClase import ComponenteClase
from back_pez.db.model.contenido import Contenido
from back_pez.db.model.horario import Horario
from back_pez.db.model.modoEnsenianza import ModoEnsenianza
from back_pez.db.model.competencia import Competencia
from back_pez.db.model.perfilEstudiante import PerfilEstudiante
from back_pez.db.model.profesor import Profesor
from back_pez.db.model.programa import Programa
from back_pez.db.model.subComponente import subComponente
from back_pez.db.model.usuario import Usuario


engine = create_engine("postgresql+psycopg2://PEZ:PEZPassword@localhost:5432/PEZDB")

if not engine.dialect.has_table(engine,Profesor.__table__):
    Profesor.__table__.drop(engine)

if not engine.dialect.has_table(engine,Competencia.__table__):
    Competencia.__table__.drop(engine)

if not engine.dialect.has_table(engine,Contenido.__table__):
    Contenido.__table__.drop(engine)

if not engine.dialect.has_table(engine,ModoEnsenianza.__table__):
    ModoEnsenianza.__table__.drop(engine)

if not engine.dialect.has_table(engine,ComponenteClase.__table__):
    ComponenteClase.__table__.drop(engine)

if not engine.dialect.has_table(engine,Horario.__table__):
    Horario.__table__.drop(engine)

if not engine.dialect.has_table(engine,Actividad.__table__):
    Actividad.__table__.drop(engine)

if not engine.dialect.has_table(engine,Asignatura.__table__):
    Asignatura.__table__.drop(engine)

if not engine.dialect.has_table(engine,Componente.__table__):
    Componente.__table__.drop(engine)

if not engine.dialect.has_table(engine,subComponente.__table__):
    subComponente.__table__.drop(engine)

if not engine.dialect.has_table(engine,PerfilEstudiante.__table__):
    PerfilEstudiante.__table__.drop(engine)

if not engine.dialect.has_table(engine,Programa.__table__):
    Programa.__table__.drop(engine)

if not engine.dialect.has_table(engine,Usuario.__table__):
    Usuario.__table__.drop(engine)