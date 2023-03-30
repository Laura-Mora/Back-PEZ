from back_pez.db.model.asignatura import Asignatura


class Componente():
    id: int
    nombre: str
    cantCreditos: int
    asignaturasObligatorias: Asignatura = []
    asignaturasElectivas: Asignatura = []