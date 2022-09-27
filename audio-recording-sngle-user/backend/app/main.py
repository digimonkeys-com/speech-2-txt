from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import texts, samples


def create_app():
    # FastAPI
    app = FastAPI(
        docs_url="/api/docs",
        version="1.0.0",
        openapi_url="/api"
    )

    app.include_router(texts.router)
    app.include_router(samples.router)

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
