from fastapi import APIRouter
from db.model.modoEnsenianza import ModoEnsenianza

router = APIRouter(prefix="/modoEnsenianza",
                   tags=["modoEnsenianza"],
                   responses={404: {"message": "No encontrado"}})

@router.get("/")
async def modosEnsenianza():
    return None

@router.get("/{id}")  # Path
async def modoEnsenianza(id: str):
    return search_modo("_id", id)


@router.get("/")  # Query
async def modoEnsenianza(id: str):
    return search_modo("_id", id)

def search_modo(field: str, key):
    try:
        #user = db_client.users.find_one({field: key})
        #return Contenido(**user_schema(contenido))
        return None
    except:
        return {"error": "No se ha encontrado el contenido"}