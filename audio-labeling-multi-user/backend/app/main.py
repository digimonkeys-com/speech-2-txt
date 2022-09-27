import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import samples, auth, recordings


def create_app():
    # FastAPI
    app = FastAPI(
        docs_url=f"{os.getenv('ROOT_PATH')}/docs",
        version="1.0.0",
        openapi_url=f"{os.getenv('ROOT_PATH')}"
    )

    app.include_router(samples.router)
    app.include_router(auth.router)
    app.include_router(recordings.router)

    # CORS middleware
    origins = [
        "*"
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
