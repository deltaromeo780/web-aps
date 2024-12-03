import uvicorn
import logging
import redis.asyncio as redis

from fastapi import FastAPI, Depends
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from fastapi.middleware.cors import CORSMiddleware

# from src.routes import contacts, auth
from src.routes import contacts, auth, users

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

origins = ["*"]
methods = ["*"]
headers = ["*"]

app.include_router(contacts.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers,
)


@app.on_event("startup")
async def startup():
    r = await redis.Redis(
        host="localhost", port=6379, db=0, encoding="utf-8", decode_responses=True
    )
    await FastAPILimiter.init(r)


@app.get("/")
def read_root():
    dict_to_return = {
        "AppName": "Contacts - lowercase",
        "Documentation": "/docs",
        "Display all contacts": "api/contacts/",
        "Display contact": "api/contacts/{contact_id: int}",
        "Display contacts with birthday upcoming": "api/contacts/birthday",
        "Display contact by choosen field": "api/contacts/byfield?field=field_name&value=value",
        "field_name": ["id", "first_name", "last_name", "email"],
    }

    return dict_to_return


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
