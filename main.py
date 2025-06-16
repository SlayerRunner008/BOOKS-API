from fastapi import FastAPI
from config.database import engine, Base
from routes import homeRoute, bookRoutes, authRoute

app = FastAPI(title="Library API", version="0.0.1")

Base.metadata.create_all(bind=engine)

app.include_router(homeRoute.router)
app.include_router(bookRoutes.router)
app.include_router(authRoute.router)
