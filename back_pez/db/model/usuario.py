from back_pez.db.model.perfilEstudiante import PerfilEstudiante
from back_pez.db.model.programa import Programa

class Programa():
    id: int
    nombre: str
    correo: str
    contrasenia: str
    programa: Programa
    tipo: str
    perfilEstudiante: PerfilEstudiante