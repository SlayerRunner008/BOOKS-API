from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from config.database import engine, Base
from routes import homeRoute, bookRoutes, authRoute
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="Biblioteca", version="0.0.1")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas
Base.metadata.create_all(bind=engine)

# Rutas API
app.include_router(homeRoute.router)
app.include_router(bookRoutes.router)
app.include_router(authRoute.router)

# Archivos estáticos (frontend)
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")
