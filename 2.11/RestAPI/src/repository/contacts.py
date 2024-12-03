from typing import List

from sqlalchemy.orm import Session

from src.database.model import Contact
from src.schemas import ContactBase

from src.repository.added_features import get_id_birthday_upcoming


async def get_contacts(db: Session) -> List[Contact]:
    return db.query(Contact).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    print("We are in repo.get_contact function")
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    return contact


async def get_contact_by_id(contact_id: str, db: Session) -> List[Contact]:
    print("We are in repo.get_contact_by_id function")
    try:
        contact_id = int(contact_id)
    except:
        print("ValueError: Contact_id must be an integer")
        return None
    else:
        return db.query(Contact).filter(Contact.id == contact_id).all()


async def get_contacts_by_first_name(
    contact_first_name: str, db: Session
) -> List[Contact]:
    print("We are in repo.get_contact_by_first_name function")
    print(f"contact_first_name = {contact_first_name}")
    contacts = db.query(Contact).filter(Contact.first_name == contact_first_name).all()
    return contacts


async def get_contacts_by_last_name(
    contact_last_name: str, db: Session
) -> List[Contact]:
    print("We are in repo.get_contact_by_last_name function")
    return db.query(Contact).filter(Contact.last_name == contact_last_name).all()


async def get_contact_by_email(contact_email: str, db: Session) -> List[Contact]:
    print("We are in repo.get_contact_by_email function")
    return db.query(Contact).filter(Contact.email == contact_email).all()


async def get_contacts_by(field: str, value: str, db: Session) -> List[Contact]:

    fields = {
        "id": get_contact_by_id,
        "first_name": get_contacts_by_first_name,
        "last_name": get_contacts_by_last_name,
        "email": get_contact_by_email,
    }

    if field in fields.keys():
        print(value)
        print(type(value))
        contacts = await fields[field](value, db)
    else:
        print("There is no such field")
        contacts = []

    return contacts


async def create_new_contact(body: ContactBase, db: Session) -> Contact:
    print("We are in repo.create_new_contact function")
    contact = Contact(
        first_name=body.first_name.lower(),
        last_name=body.last_name.lower(),
        email=body.email.lower(),
        phone=body.phone,
        born_date=body.born_date,
        additional=body.additional.lower(),
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact: Contact, body: ContactBase, db: Session):
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
    print("We are in repo.remove_contact function")
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_contacts_with_upcoming_birtday(db: Session):
    print("We are in repo.get_contact_with_upcoming_birtday function")

    born_dates = db.query(Contact).values(Contact.born_date, Contact.id)

    id_list = get_id_birthday_upcoming(born_dates)
    contacts = db.query(Contact).filter(Contact.id.in_(id_list)).all()

    return contacts
