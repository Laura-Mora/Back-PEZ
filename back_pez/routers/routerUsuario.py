from typing import List

from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi import Body
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from back_pez.db.model.usuario import UsuarioModelo
from db.model.usuario import Usuario
from back_pez.db.model.programa import Programa, ProgramaModel

from db.dbconfig import engine
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter(prefix="/usuario",
                   tags=["usuario"],
                   responses={404: {"message": "No encontrado"}})

@router.options("/")
def optionsUsuarios():
    allowed_methods = ["GET", "OPTIONS","POST"]
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": ", ".join(allowed_methods),
        "Access-Control-Allow-Headers": "Content-Type, Accept"
    }
    return Response(headers=headers)

@router.options("/signup")
def optionsUsuario():
    allowed_methods = ["GET", "OPTIONS","POST"]
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": ", ".join(allowed_methods),
        "Access-Control-Allow-Headers": "Content-Type, Accept"
    }
    return Response(headers=headers)

@router.options("/login")
def optionsUsuarioLogin():
    allowed_methods = ["GET", "OPTIONS","POST"]
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": ", ".join(allowed_methods),
        "Access-Control-Allow-Headers": "Content-Type, Accept"
    }
    return Response(headers=headers)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "tu_secret_key_aqui"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuario/login")


Session = sessionmaker(bind=engine)

@router.get("/")
def usuarios():
    session = Session()
    usuaruios = session.query(Usuario).all()
    session.close()
    return usuaruios

@router.get("/{id}")  # Path
def usuario(id: str):
    session = Session()
    usuario = session.query(Usuario).filter(Usuario.id == id).first()
    session.close()
    if not usuario:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    return usuario

@router.post('/')
def crear_usuario(id: int,nombre: str, correo: str, contrasenia: str,
    programa: List[ProgramaModel], tipo:str):
    session = Session()
    nuevo_usuario = Usuario(id=id,nombre=nombre,correo=correo, contrasenia=contrasenia,programa= programa, tipo=tipo)
    session.add(nuevo_usuario)
    session.commit()
    session.close()
    return nuevo_usuario

@router.put('/{id}')
def actualizar_usuario(id: int, usuario_update: dict):
    session = Session()
    usuario = session.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    for campo, valor in usuario_update.items():
        setattr(usuario, campo, valor)
    session.add(usuario)
    session.commit()
    session.close()
    return usuario


def verificar_password(contrasena_plana, contrasena_hash):
    return pwd_context.verify(contrasena_plana, contrasena_hash)

def generar_token_acceso(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def autenticar_usuario(usuario, contrasena):
    session = Session()
    usuario_db = session.query(Usuario).filter(Usuario.correo == usuario).first()
    session.close()

    if not usuario_db or not verificar_password(contrasena, usuario_db.contrasenia):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = generar_token_acceso(
        data={"sub": usuario_db.nombre}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=dict)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    token = autenticar_usuario(form_data.username, form_data.password)
    return token

def encriptar_password(contrasena_plana):
    return pwd_context.hash(contrasena_plana)

from fastapi import Body

@router.post("/signup")
def signup(data: dict = Body(...)):
    print("Hola")
    try:
        id = data.get("id")
        nombre = data.get("nombre")
        contrasenia = data.get("contrasenia")
        tipo = data.get("tipo")
        correo = data.get("correo")
        id_programa = data.get("id_programa")

        session = Session()

        # Verificar si el usuario ya existe
        usuario_existente = session.query(Usuario).filter(Usuario.correo == correo).first()
        if usuario_existente:
            raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")
        
        cantidad_usuarios = session.query(func.count(Usuario.id)).scalar()
        nuevo_id = cantidad_usuarios + 1

        # Encriptar la contraseña antes de guardarla
        contrasena_encriptada = encriptar_password(contrasenia)

        programas = session.query(Programa).filter(Programa.id.in_(id_programa)).all()

        # Guardar el nuevo usuario en la base de datos
        usuarioNuevo = Usuario(id = nuevo_id, nombre = nombre, correo = correo,contrasenia = contrasena_encriptada, tipo = tipo, programa = programas)
        session.add(usuarioNuevo)
        session.commit()
        session.close()

        return usuario
    except Exception as e:
        print(f"Error: {e}")
        raise

@router.post("/logout")
def logout():
    try:
        

        return {"message": "Logout exitoso"}
    except:
        raise HTTPException(status_code=400, detail="Error al realizar el logout")
    
@router.post("/perso")    
def perso(data: dict = Body(...)):
    try:
        idUsuario = data.get("idUsuario")
        profesion = data.get("profesion")
        areaDesempenio = data.get("areaDesempenio")
        motivo = data.get("motivo")
        id_asignaturas = data.get("asignaturasCursadas")
        id_tematicas = data.get("tematicasUsuario")
        id_competencias = data.get("competenciasUsuario")
        id_actividades = data.get("actividadesUsuario")
        id_horarios = data.get("horariosUsuario")
        id_modalidad = data.get("modalidadUsuario")
        id_modos = data.get("modosUsuario")
        return None
    except Exception as e:
        print(f"Error: {e}")
        raise

