from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import insert

from back_pez.db.model.profesor import Profesor

engine = create_engine("postgresql+psycopg2://PEZ:PEZPassword@localhost:5432/PEZDB")

if not engine.dialect.has_table(engine,Profesor.__table__):
    Profesor.__table__.drop(engine)
