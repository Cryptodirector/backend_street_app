import os
from app.routers.users_router import router as user_router
from app.routers.jobs_router import router as jobs_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi_redis_cache import FastApiRedisCache
from fastapi import FastAPI, Request, Response
from sqlalchemy.orm import Session

app = FastAPI()

LOCAL_REDIS_URL = "redis://127.0.0.1:6379"


@app.on_event("startup")
def startup():
    redis_cache = FastApiRedisCache()
    redis_cache.init(
        host_url=os.environ.get("REDIS_URL", LOCAL_REDIS_URL),
        prefix="myapi-cache",
        response_header="X-MyAPI-Cache",
        ignore_arg_types=[Request, Response, Session]
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(jobs_router)

