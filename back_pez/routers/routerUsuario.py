from fastapi import APIRouter
from db.model.usuario import Usuario

router = APIRouter(prefix="/usuario",
                   tags=["usuario"],
                   responses={404: {"message": "No encontrado"}})

@router.get("/", response_model=list[Usuario])
async def usuarios():
    return 

@router.get("/{id}")  # Path
async def usuario(id: str):
    return search_usuario("_id", id)


@router.get("/")  # Query
async def usuario(id: str):
    return search_usuario("_id", id)

def search_usuario(field: str, key):
    try:
        #user = db_client.users.find_one({field: key})
        #return Contenido(**user_schema(contenido))
        return
    except:
        return {"error": "No se ha encontrado el contenido"}