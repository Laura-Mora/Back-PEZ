from fastapi import APIRouter
from db.model.horario import Horario

router = APIRouter(prefix="/horario",
                   tags=["horario"],
                   responses={404: {"message": "No encontrado"}})

@router.get("/", response_model=list[Horario])
async def horarios():
    return 

@router.get("/{id}")  # Path
async def horario(id: str):
    return search_horario("_id", id)


@router.get("/")  # Query
async def horario(id: str):
    return search_horario("_id", id)

def search_horario(field: str, key):
    try:
        #user = db_client.users.find_one({field: key})
        #return Contenido(**user_schema(contenido))
        return
    except:
        return {"error": "No se ha encontrado el contenido"}