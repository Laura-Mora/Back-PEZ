from fastapi import APIRouter
from db.model.subComponente import subComponente

router = APIRouter(prefix="/componente",
                   tags=["componente"],
                   responses={404: {"message": "No encontrado"}})

@router.get("/")
async def subComponentes():
    return None

@router.get("/{id}")  # Path
async def subComponente(id: str):
    return search_subcomponente("_id", id)


@router.get("/")  # Query
async def subComponentes(id: str):
    return search_subcomponente("_id", id)

def search_subcomponente(field: str, key):
    try:
        #user = db_client.users.find_one({field: key})
        #return Contenido(**user_schema(contenido))
        return None
    except:
        return {"error": "No se ha encontrado el contenido"}