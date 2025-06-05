from fastapi import FastAPI
from api import router
import models
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Serveur REF - FastAPI")

app.mount("/static", StaticFiles(directory="static"), name="static")
# Crear las tablas al iniciar
models.create_tables()

# Incluir el router (API REST)
app.include_router(router)

