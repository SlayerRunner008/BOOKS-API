from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from config.database import engine, Base
from routes import homeRoute, bookRoutes, authRoute
#Para rutas de archivos estáticos
from fastapi.staticfiles import StaticFiles
import os
from fastapi.responses import FileResponse

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

app = FastAPI(title="Library API", version="0.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(homeRoute.router)
app.include_router(bookRoutes.router)
app.include_router(authRoute.router)
