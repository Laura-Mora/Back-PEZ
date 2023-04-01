from fastapi import APIRouter
from db.model.asignatura import Asignatura

router = APIRouter(prefix="/asignatura",
                   tags=["asignatura"],
                   responses={404: {"message": "No encontrado"}})

@router.get("/")
async def asignaturas():
    return None

@router.get("/{id}")  # Path
async def asignatura(id: str):
    return search_asignatura("_id", id)


@router.get("/")  # Query
async def asignatura(id: str):
    return search_asignatura("_id", id)

def search_asignatura(field: str, key):
    try:
        #user = db_client.users.find_one({field: key})
        #return Contenido(**user_schema(contenido))
        return None
    except:
        return {"error": "No se ha encontrado el contenido"}