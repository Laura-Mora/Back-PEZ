from back_pez.db.model.asignatura import Asignatura
from back_pez.db.model.subComponente import subComponente


class Componente():
    id: int
    nombre: str
    cantCreditos: int
    asignaturasObligatorias: Asignatura = []
    asignaturasElectivas: Asignatura = []
    subcomponentes: subComponente = []