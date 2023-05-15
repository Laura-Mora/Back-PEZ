from db.model.asignatura import Asignatura
from db.model.componente import ComponenteElectiva, ComponenteModelo, ComponenteObligactoria, ComponenteSubComponente
from db.model.subComponente import subComponente
from db.model.componente import Componente
from sqlalchemy.orm import sessionmaker
from db.dbconfig import engine
from sqlalchemy import exists

Session = sessionmaker(bind=engine)

def crear_componente(response:ComponenteModelo):
    if not response.asignaturasObligatorias and not response.asignaturasElectivas and not response.subcomponentes:
        raise Exception('No hay oligatorias, electivas o subcomponente') 
    
    session = Session()
    
    nuevo_componente = Componente(id=response.id,nombre=response.nombre,cantCreditos=response.cantCreditos)
    session.add(nuevo_componente)
    session.commit()

    if response.asignaturasObligatorias:
        obligatorias = [asignatura.id for asignatura in response.asignaturasObligatorias]
        asiganturasOb = session.query(Asignatura).filter(Asignatura.id.in_(obligatorias)).all()
        componente = session.query(Componente).filter(Componente.id == response.id).first()
        nuevo_componenteOb = ComponenteObligactoria(componente_id=componente.id, componente=componente,asignaturasObligatorias=asiganturasOb)
        session.add(nuevo_componenteOb)
    if response.asignaturasElectivas:
        electivas = [asignatura.id for asignatura in response.asignaturasElectivas]
        asignaturasEl = session.query(Asignatura).filter(Asignatura.id.in_(electivas)).all()
        componente = session.query(Componente).filter(Componente.id == response.id).first()
        nuevo_componenteEl = ComponenteElectiva(componente_id=componente.id,componente=componente,asignaturasElectivas=asignaturasEl)
        session.add(nuevo_componenteEl)
    if response.subcomponentes:
        subcomponentes_ids = [sub.id for sub in response.subcomponentes]
        subcomponentes = session.query(subComponente).filter(subComponente.id.in_(subcomponentes_ids)).all()
        componenteEn = session.query(Componente).filter(Componente.id == response.id).first()
        nuevo_componenteSub = ComponenteSubComponente(subcomponentes=subcomponentes,componente_id=componenteEn.id,componente=componenteEn)
        session.add(nuevo_componenteSub)

    session.commit()
    session.close()
    return nuevo_componente
        


