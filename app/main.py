from fastapi import FastAPI

from app.database import engine
from app.models import Base
from app.routers import usuarios, exercicios, fichas

app = FastAPI()

app.include_router(usuarios.router)
app.include_router(exercicios.router)
app.include_router(fichas.router)


    
    


