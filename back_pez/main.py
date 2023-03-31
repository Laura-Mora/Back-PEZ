from fastapi import FastAPI
from routers import routerActividad, routerAsignatura, routerCompetencia, routerComponente, routerComponenteClase, routerContenido, routerHorario, routerModoEnsenianza, routerPerfilEstudiante, routerProfesor, routerPrograma, routerSubComponente, routerUsuario

app = FastAPI()

app.include_router(routerActividad.router)
app.include_router(routerAsignatura.router)
app.include_router(routerCompetencia.router)
app.include_router(routerComponente.router)
app.include_router(routerComponenteClase.router)
app.include_router(routerContenido.router)
app.include_router(routerHorario.router)
app.include_router(routerModoEnsenianza.router)
app.include_router(routerPerfilEstudiante.router)
app.include_router(routerProfesor.router)
app.include_router(routerPrograma.router)
app.include_router(routerSubComponente.router)
app.include_router(routerUsuario.router)