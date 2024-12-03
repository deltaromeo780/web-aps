from typing import List

from fastapi import Depends, APIRouter, status  # HTTPException,
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.schemas import ContactBase, ContactResponse
from src.repository.added_features import get_no_contacts_exception
from src.services.auth import auth_service
from src.database.model import User

import src.repository.contacts as contact_repo

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/",
            response_model=List[ContactResponse],
            description="No more than 10 requests per minute",
            dependencies=[Depends(RateLimiter(times=10, seconds=60))],
            )
async def display_all_contacts(
        db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user),
):
    print("We are in routes.display_all_contacts function")
    contacts = await contact_repo.get_contacts(db, current_user)
    print(contacts)
    return contacts


@router.get("/birthday",
            response_model=List[ContactResponse],
            description="No more than 10 requests per minute",
            dependencies=[Depends(RateLimiter(times=10, seconds=60))],
            )
async def display_contacts_with_upcoming_birthay(
        db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user),
):
    print("We are in routes.display_contacts_with_upcoming_birthay function")
    contacts = await contact_repo.get_contacts_with_upcoming_birtday(db, current_user)
    print(contacts)
    return contacts


@router.get("/byfield",
            response_model=List[ContactResponse],
            description="No more than 10 requests per minute",
            dependencies=[Depends(RateLimiter(times=10, seconds=60))],
            )
async def display_choosen_contacts(
        field: str,
        value: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user),
):
    print("We are in routes.display_choosen_contacts function")
    contacts = await contact_repo.get_contacts_by(field, value, db, current_user)
    get_no_contacts_exception(contacts)
    return contacts


@router.get("/{contact_id}",
            response_model=ContactResponse,
            description="No more than 10 requests per minute",
            dependencies=[Depends(RateLimiter(times=10, seconds=60))],
            )
async def display_choosen_contact_by_id(
        contact_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user),
):
    print("We are in routes.display_choosen_contact_by_id function")
    contact = await contact_repo.get_contact(contact_id, db, current_user)
    get_no_contacts_exception(contact)
    return contact


@router.post("/", response_model=ContactResponse,
             status_code=status.HTTP_201_CREATED,
             description="No more than 5 requests per minute",
             dependencies=[Depends(RateLimiter(times=5, seconds=60))],
             )
async def add_new_contact(
        body: ContactBase,
        db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user),
):
    print("We are in routes.add_new_contact function")
    new_contact = await contact_repo.create_new_contact(body, db, current_user)

    return new_contact


@router.put("/{contact_id}", response_model=ContactResponse,
            description="No more than 10 requests per minute",
            dependencies=[Depends(RateLimiter(times=10, seconds=60))],
            )
async def update_choosen_contact(
        contact_id: int,
        body: ContactBase,
        db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user),
):
    print("We are in routes.update_choosen_contact function")
    contact = await contact_repo.get_contact(contact_id, db, current_user)

    get_no_contacts_exception(contact)
    print(f"contact_to_update = {contact}")
    updated_contact = await contact_repo.update_contact(contact, body, db)
    return updated_contact


@router.delete("/{contact_id}",
               response_model=ContactResponse,
               description="No more than 10 requests per minute",
               dependencies=[Depends(RateLimiter(times=10, seconds=60))],
               )
async def remove_choosen_contact(
        contact_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user),
):
    print("We are in routes.remove_choosen_contact function")
    contact = await contact_repo.get_contact(contact_id, db, current_user)

    get_no_contacts_exception(contact)
    removed_contact = await contact_repo.remove_contact(contact, db)
    return removed_contact
