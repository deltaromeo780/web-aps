import uvicorn
import logging
import redis.asyncio as redis

from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter

from fastapi.middleware.cors import CORSMiddleware


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
    """
       Asynchronous function for initializing resources at application startup.

       This function initializes a connection to Redis and initializes the FastAPILimiter
       using the provided Redis connection.

       Returns:
           None

       Raises:
           Any exceptions raised by Redis initialization or FastAPILimiter initialization.
       """
    r = await redis.Redis(
        host="localhost", port=6379, db=0, encoding="utf-8", decode_responses=True
    )
    await FastAPILimiter.init(r)


@app.get("/")
def read_root():
    """
       Function to retrieve the root information for the Contacts application.

       This function returns a dictionary containing key-value pairs representing
       various endpoints and information related to the Contacts application.

       Returns:
           dict: A dictionary containing the following key-value pairs:
               - "AppName": The name of the application ("Contacts - lowercase").
               - "Documentation": The URL for the API documentation ("/docs").
               - "Display all contacts": The URL for displaying all contacts ("api/contacts/").
               - "Display contact": The URL pattern for displaying a specific contact
                                     ("api/contacts/{contact_id: int}").
               - "Display contacts with birthday upcoming": The URL for displaying contacts
                                                            with upcoming birthdays
                                                            ("api/contacts/birthday").
               - "Display contact by chosen field": The URL pattern for displaying contacts
                                                     based on a chosen field
                                                     ("api/contacts/byfield?field=field_name&value=value").
               - "field_name": A list of available field names for querying contacts
                               (["id", "first_name", "last_name", "email"]).
       """
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
