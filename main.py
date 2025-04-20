# main.py
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from blogs.api.api import api_router
from blogs.db.database import database
from blogs.configs.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield
    await shutdown()


app = FastAPI(
    title="Blogs API",
    # description=" APIs for blogs posting and update",
    version="1.0",
    docs_url=f"{settings.API_PREFIX}/docs",
    swagger_ui_oauth2_redirect_url=f"{settings.API_PREFIX}/openapi.json",
    lifespan=lifespan
)

app.include_router(api_router, prefix=settings.API_PREFIX)


async def startup():
    # security.auth0_jwks = await http.get(Setting.AUTH0_JWKS_URL)
    await database.connect()
    print ("Service is UP")


async def shutdown():
    await database.disconnect()


@app.get("/health", include_in_schema=False)
async def health():
    return "Alive"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=settings.APP_PORT, log_config=None)
