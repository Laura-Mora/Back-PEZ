from fastapi import APIRouter
from db.model.actividad import Actividad

router = APIRouter(prefix="/actividad",
                   tags=["actividad"],
                   responses={404: {"message": "No encontrado"}})

@router.get("/", response_model=list[Actividad])
async def actividades():
    return 

@router.get("/{id}")  # Path
async def actividad(id: str):
    return search_actividad("_id", id)


@router.get("/")  # Query
async def actividad(id: str):
    return search_actividad("_id", id)

def search_actividad(field: str, key):
    try:
        #user = db_client.users.find_one({field: key})
        #return Contenido(**user_schema(contenido))
        return
    except:
        return {"error": "No se ha encontrado el contenido"}