from fastapi import FastAPI
from api import router
import models

app = FastAPI(title="Serveur REF - FastAPI")

# Crear las tablas al iniciar
models.create_tables()

# Incluir el router (API REST)
app.include_router(router)

# Puedes ejecutar con:
# uvicorn main:app --reload
