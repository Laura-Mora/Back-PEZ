from fastapi import APIRouter
from db.model.contenido import Contenido

router = APIRouter(prefix="/contenido",
                   tags=["contenido"],
                   responses={404: {"message": "No encontrado"}})

@router.get("/", response_model=list[Contenido])
async def contenidos():
    return 

@router.get("/{id}")  # Path
async def contenido(id: str):
    return search_contenido("_id", id)


@router.get("/")  # Query
async def contenido(id: str):
    return search_contenido("_id", id)

def search_contenido(field: str, key):
    try:
        #user = db_client.users.find_one({field: key})
        #return Contenido(**user_schema(contenido))
        return
    except:
        return {"error": "No se ha encontrado el contenido"}