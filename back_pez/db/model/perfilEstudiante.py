from back_pez.db.model.actividad import Actividad
from back_pez.db.model.asignatura import Asignatura
from back_pez.db.model.competencia import Competencia
from back_pez.db.model.componenteClase import ComponenteClase
from back_pez.db.model.contenido import Contenido
from back_pez.db.model.horario import Horario
from back_pez.db.model.modoEnsenianza import ModoEnsenianza


class PerfilEstudiante():
    id: int
    profesion: str
    javeriano: bool
    semestre: int
    areaDesempenio: str
    asignaturasCursadas: Asignatura = []
    asignaturasGustadas: Asignatura = []
    modalidadPreferencia: ComponenteClase
    modoEnsenianzaPreferencia: ModoEnsenianza
    horariosPreferencias: Horario = []
    competenciasGusto: Competencia = []
    actividadesGusto: Actividad = []
    tematicasGusto: Contenido = []