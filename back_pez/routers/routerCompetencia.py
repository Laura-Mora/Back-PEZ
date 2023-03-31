from fastapi import APIRouter
from db.model.competencia import Competencia

router = APIRouter(prefix="/competencia",
                   tags=["competencia"],
                   responses={404: {"message": "No encontrado"}})

@router.get("/", response_model=list[Competencia])
async def competencias():
    return 

@router.get("/{id}")  # Path
async def competencia(id: str):
    return search_competencia("_id", id)


@router.get("/")  # Query
async def competencia(id: str):
    return search_competencia("_id", id)

def search_competencia(field: str, key):
    try:
        #user = db_client.users.find_one({field: key})
        #return Contenido(**user_schema(contenido))
        return
    except:
        return {"error": "No se ha encontrado el contenido"}