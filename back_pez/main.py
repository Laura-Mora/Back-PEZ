from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from routers import routerActividad, routerAsignatura, routerCompetencia, routerComponente, routerComponenteClase, routerContenido, routerHorario, routerModoEnsenianza, routerPerfilEstudiante, routerProfesor, routerPrograma, routerSubComponente, routerUsuario, routerResenia
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:8100",  # Reemplaza con el origen deseado
]

app.include_router(routerActividad.router)
app.include_router(routerCompetencia.router)
app.include_router(routerComponente.router)
app.include_router(routerComponenteClase.router)
app.include_router(routerContenido.router)
app.include_router(routerHorario.router)
app.include_router(routerModoEnsenianza.router)
app.include_router(routerAsignatura.router)
app.include_router(routerPerfilEstudiante.router)
app.include_router(routerProfesor.router)
app.include_router(routerPrograma.router)
app.include_router(routerSubComponente.router)
app.include_router(routerUsuario.router)
app.include_router(routerResenia.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)