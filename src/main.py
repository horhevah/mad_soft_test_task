from fastapi import FastAPI

from src.auth.schemas import UserRead, UserCreate
from src.auth.users import fastapi_users, auth_backend
# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend
# from redis import asyncio as aioredis

# from auth.base_config import auth_backend, fastapi_users
# from auth.schemas import UserCreate, UserRead
from src.memes.router import router as memes_router
from fastapi_pagination import Page, add_pagination


app = FastAPI(
    title="Memes App"
)

app.include_router(memes_router)
add_pagination(app)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# app.include_router(
#     fastapi_users.get_auth_router(auth_backend),
#     prefix="/auth",
#     tags=["Auth"],
# )
#
# app.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix="/auth",
#     tags=["Auth"],
# )

# app.include_router(router_operation)
# app.include_router(router_tasks)
#
#
# @app.on_event("startup")
# async def startup_event():
#     redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
