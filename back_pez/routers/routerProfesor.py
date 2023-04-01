from fastapi import APIRouter
from db.model.profesor import Profesor

router = APIRouter(prefix="/profesor",
                   tags=["profesor"],
                   responses={404: {"message": "No encontrado"}})

@router.get("/")
async def profesores():
    return None

@router.get("/{id}")  # Path
async def profesor(id: str):
    return search_profesor("_id", id)


@router.get("/")  # Query
async def profesor(id: str):
    return search_profesor("_id", id)

def search_profesor(field: str, key):
    try:
        #user = db_client.users.find_one({field: key})
        #return Contenido(**user_schema(contenido))
        return None
    except:
        return {"error": "No se ha encontrado el contenido"}