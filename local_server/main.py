# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from core import lifespan
import auth_routes, api_routes
from config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Diabetes Detection Client Server", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)

def include_routers(app: FastAPI, routers: list):
    for router in routers:
        app.include_router(router)

routers = [auth_routes.router, api_routes.router]
include_routers(app, routers)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
