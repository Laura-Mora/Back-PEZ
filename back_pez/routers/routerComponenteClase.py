from fastapi import APIRouter
from db.model.componenteClase import ComponenteClase

router = APIRouter(prefix="/componenteClase",
                   tags=["componenteClase"],
                   responses={404: {"message": "No encontrado"}})

@router.get("/", response_model=list[ComponenteClase])
async def componentesClase():
    return 

@router.get("/{id}")  # Path
async def componenteClase(id: str):
    return search_componenteClase("_id", id)


@router.get("/")  # Query
async def componenteClase(id: str):
    return search_componenteClase("_id", id)

def search_componenteClase(field: str, key):
    try:
        #user = db_client.users.find_one({field: key})
        #return Contenido(**user_schema(contenido))
        return
    except:
        return {"error": "No se ha encontrado el contenido"}