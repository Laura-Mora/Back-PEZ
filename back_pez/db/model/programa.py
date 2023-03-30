from back_pez.db.model.componente import Componente


class Programa():
    id: int
    nombre: str
    cantCreditos: int
    componentes: Componente = []
    
    