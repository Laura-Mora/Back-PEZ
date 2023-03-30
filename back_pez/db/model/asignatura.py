from back_pez.db.model.actividad import Actividad
from back_pez.db.model.competencia import Competencia
from back_pez.db.model.componenteClase import ComponenteClase
from back_pez.db.model.contenido import Contenido
from back_pez.db.model.horario import Horario
from back_pez.db.model.modoEnsenianza import ModoEnsenianza
from back_pez.db.model.profesor import Profesor


class Asignatura():
    id: int
    nombre: str
    poblacionObjetivo: str
    creditos: int
    complejidad: str
    modalidad: ComponenteClase
    profesores: Profesor =[]
    modoEnsenianza: ModoEnsenianza
    horarios: Horario = []
    competencias: Competencia = []
    actividades: Actividad = []
    tematicas: Contenido = []