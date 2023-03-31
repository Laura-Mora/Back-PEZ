from fastapi import APIRouter
from db.model.programa import Programa

router = APIRouter(prefix="/programa",
                   tags=["programa"],
                   responses={404: {"message": "No encontrado"}})

@router.get("/", response_model=list[Programa])
async def programas():
    return 

@router.get("/{id}")  # Path
async def programa(id: str):
    return search_programa("_id", id)


@router.get("/")  # Query
async def programa(id: str):
    return search_programa("_id", id)

def search_programa(field: str, key):
    try:
        #user = db_client.users.find_one({field: key})
        #return Contenido(**user_schema(contenido))
        return
    except:
        return {"error": "No se ha encontrado el contenido"}