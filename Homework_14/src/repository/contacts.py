from typing import List

from sqlalchemy.orm import Session

from src.database.model import Contact, User
from src.schemas import ContactBase

from src.repository.added_features import get_id_birthday_upcoming


async def get_contacts(db: Session, user: User) -> List[Contact]:
    """
       Asynchronous function to retrieve contacts associated with a specific user from the database.

       This function queries the database session to retrieve all contacts that belong to the specified user.

       Args:
           db (Session): The database session to perform the query on.
           user (User): The user object for whom to retrieve contacts.

       Returns:
           List[Contact]: A list of Contact objects associated with the specified user.

       Example:
           To retrieve all contacts associated with a specific user:
           contacts = await get_contacts(db, user_object)
       """
    return db.query(Contact).filter(Contact.user_id == user.id).all()


async def get_contact(contact_id: int, db: Session, user: User) -> Contact:
    """
        Asynchronous function to retrieve a specific contact associated with a user from the database.

        This function queries the database session to retrieve the contact with the specified ID,
        belonging to the specified user.

        Args:
            contact_id (int): The ID of the contact to retrieve.
            db (Session): The database session to perform the query on.
            user (User): The user object to whom the contact belongs.

        Returns:
            Contact: The Contact object with the specified ID and belonging to the specified user,
            or None if no such contact is found.

        Example:
            To retrieve a specific contact associated with a user by its ID:
            contact = await get_contact(contact_id, db, user_object)
        """
    print("We are in repo.get_contact function")
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user.id).first()
    return contact


async def get_contact_by_id(contact_id: str, db: Session, user: User) -> List[Contact]:
    """
       Asynchronous function to retrieve a contact by ID associated with a specific user from the database.

       This function attempts to convert the provided contact_id to an integer. If successful,
       it queries the database session to retrieve the contact with the specified ID, belonging
       to the specified user.

       Args:
           contact_id (str): The ID of the contact to retrieve (as a string).
           db (Session): The database session to perform the query on.
           user (User): The user object to whom the contact belongs.

       Returns:
           List[Contact] or None: A list containing the Contact object with the specified ID
           and belonging to the specified user, if found. Returns None if the contact_id cannot
           be converted to an integer or if no such contact is found.

       Example:
           To retrieve a contact associated with a user by its ID:
           contacts = await get_contact_by_id("123", db, user_object)
       """
    print("We are in repo.get_contact_by_id function")
    try:
        contact_id = int(contact_id)
    except:
        print("ValueError: Contact_id must be an integer")
        return None
    else:
        return db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user.id).all()


async def get_contacts_by_first_name(
    contact_first_name: str, db: Session, user: User
) -> List[Contact]:
    """
     Asynchronous function to retrieve contacts by first name associated with a specific user from the database.

     This function queries the database session to retrieve contacts with the specified first name,
     belonging to the specified user.

     Args:
         contact_first_name (str): The first name of the contacts to retrieve.
         db (Session): The database session to perform the query on.
         user (User): The user object to whom the contacts belong.

     Returns:
         List[Contact]: A list of Contact objects with the specified first name and belonging to the specified user.

     Example:
         To retrieve contacts associated with a user by their first name:
         contacts = await get_contacts_by_first_name("John", db, user_object)
     """
    print("We are in repo.get_contact_by_first_name function")
    print(f"contact_first_name = {contact_first_name}")
    contacts = db.query(Contact).filter(Contact.first_name == contact_first_name, Contact.user_id == user.id).all()
    return contacts


async def get_contacts_by_last_name(
    contact_last_name: str, db: Session, user: User
) -> List[Contact]:
    """
       Asynchronous function to retrieve contacts by last name associated with a specific user from the database.

       This function queries the database session to retrieve contacts with the specified last name,
       belonging to the specified user.

       Args:
           contact_last_name (str): The last name of the contacts to retrieve.
           db (Session): The database session to perform the query on.
           user (User): The user object to whom the contacts belong.

       Returns:
           List[Contact]: A list of Contact objects with the specified last name and belonging to the specified user.

       Example:
           To retrieve contacts associated with a user by their last name:
           contacts = await get_contacts_by_last_name("Doe", db, user_object)
       """
    print("We are in repo.get_contact_by_last_name function")
    return db.query(Contact).filter(Contact.last_name == contact_last_name, Contact.user_id == user.id).all()


async def get_contact_by_email(contact_email: str, db: Session, user: User) -> List[Contact]:
    """
        Asynchronous function to retrieve contacts by email associated with a specific user from the database.

        This function queries the database session to retrieve contacts with the specified email address,
        belonging to the specified user.

        Args:
            contact_email (str): The email address of the contacts to retrieve.
            db (Session): The database session to perform the query on.
            user (User): The user object to whom the contacts belong.

        Returns:
            List[Contact]: A list of Contact objects with the specified email address and belonging to the specified user.

        Example:
            To retrieve contacts associated with a user by their email address:
            contacts = await get_contact_by_email("john@example.com", db, user_object)
        """
    print("We are in repo.get_contact_by_email function")
    return db.query(Contact).filter(Contact.email == contact_email, Contact.user_id == user.id).all()


async def get_contacts_by(field: str, value: str, db: Session, user: User) -> List[Contact]:
    """
        Asynchronous function to retrieve contacts by a specific field associated with a specific user from the database.

        This function allows retrieving contacts based on various fields such as 'id', 'first_name', 'last_name', or 'email'.
        It dispatches the retrieval to the corresponding functions based on the provided field.

        Args:
            field (str): The field by which to filter the contacts ('id', 'first_name', 'last_name', or 'email').
            value (str): The value to filter the contacts by.
            db (Session): The database session to perform the query on.
            user (User): The user object to whom the contacts belong.

        Returns:
            List[Contact]: A list of Contact objects filtered by the specified field and value,
            belonging to the specified user.

        Example:
            To retrieve contacts associated with a user by their first name:
            contacts = await get_contacts_by("first_name", "John", db, user_object)

            To retrieve contacts associated with a user by their email address:
            contacts = await get_contacts_by("email", "john@example.com", db, user_object)
        """

    fields = {
        "id": get_contact_by_id,
        "first_name": get_contacts_by_first_name,
        "last_name": get_contacts_by_last_name,
        "email": get_contact_by_email,
    }

    if field in fields.keys():
        print(value)
        print(type(value))
        contacts = await fields[field](value, db, user)
    else:
        print("There is no such field")
        contacts = []

    return contacts


async def create_new_contact(body: ContactBase, db: Session, user: User) -> Contact:
    """
       Asynchronous function to create a new contact associated with a specific user in the database.

       This function creates a new contact in the database using the provided contact model object.
       It sets the user ID of the contact to the ID of the specified user, then adds the new contact
       to the database session, commits the transaction, refreshes the contact object to ensure it
       reflects the latest state from the database, and finally returns the newly created contact.

       Args:
           body (ContactBase): The contact model object containing the data for the new contact.
           db (Session): The database session to perform the creation operation on.
           user (User): The user object to whom the new contact belongs.

       Returns:
           Contact: The newly created contact object.

       Example:
           To create a new contact with the provided contact model data associated with a specific user:
           new_contact = await create_new_contact(contact_model_data, db, user_object)
       """
    print("We are in repo.create_new_contact function")
    contact = Contact(
        first_name=body.first_name.lower(),
        last_name=body.last_name.lower(),
        email=body.email.lower(),
        phone=body.phone,
        born_date=body.born_date,
        additional=body.additional.lower(),
        user_id=user.id
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact: Contact, body: ContactBase, db: Session):
    """
       Asynchronous function to update an existing contact in the database.

       This function updates the attributes of an existing contact in the database
       using the data provided in the contact model object. It then commits the
       transaction to save the changes to the database.

       Args:
           contact (Contact): The existing contact object to update.
           body (ContactBase): The contact model object containing the updated data.
           db (Session): The database session to perform the update operation on.

       Returns:
           Contact: The updated contact object.

       Example:
           To update an existing contact with the provided contact model data:
           updated_contact = await update_contact(existing_contact_object, updated_contact_model_data, db)
       """
    print("We are in repo.update_contact function")

    if contact:
        contact.first_name = body.first_name.lower()
        contact.last_name = body.last_name.lower()
        contact.email = body.email.lower()
        contact.phone = body.phone
        contact.born_date = body.born_date
        contact.additional = body.additional.lower()

        db.commit()
    return contact


async def remove_contact(contact: Contact, db: Session):
    """
        Asynchronous function to remove a contact from the database.

        This function removes the specified contact from the database by deleting
        it from the session. It then commits the transaction to save the changes
        to the database.

        Args:
            contact (Contact): The contact object to remove from the database.
            db (Session): The database session to perform the removal operation on.

        Returns:
            Contact: The removed contact object.

        Example:
            To remove a contact from the database:
            removed_contact = await remove_contact(contact_object, db)
        """
    print("We are in repo.remove_contact function")
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_contacts_with_upcoming_birtday(db: Session, user: User):
    """
       Asynchronous function to retrieve contacts with upcoming birthdays associated with a specific user from the database.

       This function queries the database session to retrieve contacts with upcoming birthdays within the next 7 days,
       belonging to the specified user.

       Args:
           db (Session): The database session to perform the query on.
           user (User): The user object to whom the contacts belong.

       Returns:
           List[Contact]: A list of Contact objects with upcoming birthdays within the next 7 days, belonging to the specified user.

       Example:
           To retrieve contacts associated with a user with upcoming birthdays:
           contacts = await get_contacts_with_upcoming_birthday(db, user_object)
       """
    print("We are in repo.get_contact_with_upcoming_birtday function")

    born_dates = db.query(Contact).values(Contact.born_date, Contact.id)

    id_list = get_id_birthday_upcoming(born_dates)
    contacts = db.query(Contact).filter(Contact.id.in_(id_list), Contact.user_id==user.id).all()

    return contacts

