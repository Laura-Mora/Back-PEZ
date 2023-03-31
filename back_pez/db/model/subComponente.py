
from back_pez.db.model.asignatura import Asignatura


class subComponente():
    id: int
    nombre: str
    cantCreditos: int
    cantAsignaturas: int
    asignaturasObligatorias: Asignatura = []
    asignaturasElectivas: Asignatura = []