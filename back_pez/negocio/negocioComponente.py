from back_pez.db.model.componente import ComponenteElectiva, ComponenteModelo, ComponenteObligactoria, ComponenteSubComponente
from db.model.componente import Componente
from sqlalchemy.orm import sessionmaker
from db.dbconfig import engine

Session = sessionmaker(bind=engine)

def crear_componente(id: int,nombre: str, cantCreditos:int ,obligatoras=[], electivas=[], subcomponente=[])->ComponenteModelo:
    if not obligatoras and not electivas and not subcomponente:
        raise Exception('No hay oligatorias, electivas o subcomponente') 
    

    with Session() as session:
        nuevo_componente = Componente(id=id,nombre=nombre,cantCreditos=cantCreditos)
        session.add(nuevo_componente)
        
        if obligatoras:
            nuevo_componenteOb = ComponenteObligactoria(id=nuevo_componente.id, asignaturasObligatorias=obligatoras)
            session.add(nuevo_componenteOb)
        if electivas:
            nuevo_componenteEl = ComponenteElectiva(asignaturasElectivas=electivas)
            session.add(nuevo_componenteEl)
        if subcomponente:
            nuevo_componenteSub = ComponenteSubComponente(subcomponentes=subcomponente)
            session.add(nuevo_componenteSub)

    return ComponenteModelo(id=nuevo_componente.id, 
                            nombre=nuevo_componente.nombre, 
                            cantCreditos=nuevo_componente.cantCreditos,
                            asignaturasObligatorias=obligatoras,
                            asignaturasElectivas=electivas,
                            subcomponentes=subcomponente
                            )
        


