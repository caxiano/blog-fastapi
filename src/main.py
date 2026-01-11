from fastapi import FastAPI, Request
from src.exceptions import NotFoundPostError
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from fastapi.responses import JSONResponse
from src.controllers import auth, post
from src.database import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

tags_metadata = [
    {
        "name": "auth",
        "description": "Operations for authentication",
    },
    {
        "name": "post",
        "description": "Operations for maintaining posts.",
        "externalDocs": {
            "description": "External documentation for Posts.api",
            "url": "https://post-api.com/",
        },
    },
]

servers = [
    {
        "url": "http://localhost:8000", 
        "description": "Development environment"
    },
    {
        "url": "https://blog-fastapi-gf52.onrender.com",
        "description": "Production environment",
    },
]


app = FastAPI(
    title="DIO blog API",
    version="1.2.0",
    summary="API for personal blog.",
    description="""
DIO blog API helps you create your personal blog. 🚀

## Posts

You will be able to:

* **Create posts**.
* **Retrieve posts**.
* **Retrieve posts by ID**.
* **Update posts**.
* **Delete posts**.
* **Limit the number of daily posts** (_not implemented_).
                """,
    openapi_tags=tags_metadata,
    servers=servers,
    redoc_url=None,
    # openapi_url=None, # disable docs
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["auth"])
app.include_router(post.router, tags=["posts"])


@app.exception_handler(NotFoundPostError)
async def not_found_post_exception_handler(request: Request, exc: NotFoundPostError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )