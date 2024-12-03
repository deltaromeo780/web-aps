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
    """
        Endpoint to display all contacts associated with the current user.

        This route retrieves all contacts associated with the current authenticated user
        from the database. It implements rate limiting to ensure that no more than 10 requests
        are made per minute.

        Args:
            db (Session): The database session. Defaults to Depends(get_db).
            current_user (User): The current authenticated user obtained from the access token.

        Returns:
            List[ContactResponse]: A list of contact objects belonging to the current user.

        Raises:
            HTTPException: If there's an error during the retrieval of contacts.
        """
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
    """
      Endpoint to display contacts with upcoming birthdays associated with the current user.

      This route retrieves contacts with upcoming birthdays (within the next 7 days) associated
      with the current authenticated user from the database. It implements rate limiting to ensure
      that no more than 10 requests are made per minute.

      Args:
          db (Session): The database session. Defaults to Depends(get_db).
          current_user (User): The current authenticated user obtained from the access token.

      Returns:
          List[ContactResponse]: A list of contact objects with upcoming birthdays belonging to the current user.

      Raises:
          HTTPException: If there's an error during the retrieval of contacts with upcoming birthdays.
      """
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
    """
        Endpoint to display contacts based on a chosen field and value associated with the current user.

        This route retrieves contacts associated with the current authenticated user from the database
        based on a specified field and value. It implements rate limiting to ensure that no more than
        10 requests are made per minute.

        Args:
            field (str): The field based on which contacts are filtered (e.g., 'first_name', 'last_name').
            value (str): The value used for filtering contacts based on the specified field.
            db (Session): The database session. Defaults to Depends(get_db).
            current_user (User): The current authenticated user obtained from the access token.

        Returns:
            List[ContactResponse]: A list of contact objects filtered based on the specified field and value.

        Raises:
            HTTPException: If there's an error during the retrieval of contacts or if no contacts are found.
        """
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
    """
       Endpoint to display a specific contact by its ID associated with the current user.

       This route retrieves a specific contact associated with the current authenticated user
       from the database based on its ID. It implements rate limiting to ensure that no more
       than 10 requests are made per minute.

       Args:
           contact_id (int): The ID of the contact to be retrieved.
           db (Session): The database session. Defaults to Depends(get_db).
           current_user (User): The current authenticated user obtained from the access token.

       Returns:
           ContactResponse: The contact object corresponding to the provided contact ID.

       Raises:
           HTTPException: If there's an error during the retrieval of the contact or if no contact is found.
       """
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
    """
        Endpoint to add a new contact for the current user.

        This route allows the current authenticated user to add a new contact to their list
        of contacts in the database. It implements rate limiting to ensure that no more than
        5 requests are made per minute.

        Args:
            body (ContactBase): The request body containing the details of the new contact.
            db (Session): The database session. Defaults to Depends(get_db).
            current_user (User): The current authenticated user obtained from the access token.

        Returns:
            ContactResponse: The newly created contact object.

        Raises:
            HTTPException: If there's an error during the creation of the new contact.
        """
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
    """
        Endpoint to update a specific contact by its ID for the current user.

        This route allows the current authenticated user to update the details of a specific contact
        in their list of contacts in the database based on its ID. It implements rate limiting to ensure
        that no more than 10 requests are made per minute.

        Args:
            contact_id (int): The ID of the contact to be updated.
            body (ContactBase): The request body containing the updated details of the contact.
            db (Session): The database session. Defaults to Depends(get_db).
            current_user (User): The current authenticated user obtained from the access token.

        Returns:
            ContactResponse: The updated contact object.

        Raises:
            HTTPException: If there's an error during the update of the contact or if no contact is found.
        """
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
    """
        Endpoint to remove a specific contact by its ID for the current user.

        This route allows the current authenticated user to remove a specific contact from their list
        of contacts in the database based on its ID. It implements rate limiting to ensure that no more
        than 10 requests are made per minute.

        Args:
            contact_id (int): The ID of the contact to be removed.
            db (Session): The database session. Defaults to Depends(get_db).
            current_user (User): The current authenticated user obtained from the access token.

        Returns:
            ContactResponse: The removed contact object.

        Raises:
            HTTPException: If there's an error during the removal of the contact or if no contact is found.
        """
    print("We are in routes.remove_choosen_contact function")
    contact = await contact_repo.get_contact(contact_id, db, current_user)

    get_no_contacts_exception(contact)
    removed_contact = await contact_repo.remove_contact(contact, db)
    return removed_contact
