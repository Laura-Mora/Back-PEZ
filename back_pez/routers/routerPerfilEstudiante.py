from fastapi import APIRouter
from db.model.perfilEstudiante import PerfilEstudiante

router = APIRouter(prefix="/perfilEstudiante",
                   tags=["perfilEstudiante"],
                   responses={404: {"message": "No encontrado"}})

@router.get("/", response_model=list[PerfilEstudiante])
async def perfilesEstudiante():
    return 

@router.get("/{id}")  # Path
async def perfilEstudiante(id: str):
    return search_perfilEstudiante("_id", id)


@router.get("/")  # Query
async def perfilEstudiante(id: str):
    return search_perfilEstudiante("_id", id)

def search_perfilEstudiante(field: str, key):
    try:
        #user = db_client.users.find_one({field: key})
        #return Contenido(**user_schema(contenido))
        return
    except:
        return {"error": "No se ha encontrado el contenido"}