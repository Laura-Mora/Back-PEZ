from fastapi import APIRouter
from db.model.componente import Componente

router = APIRouter(prefix="/componente",
                   tags=["componente"],
                   responses={404: {"message": "No encontrado"}})

@router.get("/", response_model=list[Componente])
async def componentes():
    return 

@router.get("/{id}")  # Path
async def componentes(id: str):
    return search_componente("_id", id)


@router.get("/")  # Query
async def componentes(id: str):
    return search_componente("_id", id)

def search_componente(field: str, key):
    try:
        #user = db_client.users.find_one({field: key})
        #return Contenido(**user_schema(contenido))
        return
    except:
        return {"error": "No se ha encontrado el contenido"}