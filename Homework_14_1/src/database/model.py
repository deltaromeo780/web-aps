from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey


Base = declarative_base()


class Contact(Base):
    """
      Database model representing a contact entry.

      This class defines the structure of the 'contacts' table in the database,
      including various attributes such as id, first_name, last_name, email, phone,
      born_date, additional information, and user_id.

      Attributes:
          id (int): The primary key of the contact, auto-incremented.
          first_name (str): The first name of the contact (maximum length: 50 characters).
          last_name (str): The last name of the contact (maximum length: 50 characters).
          email (str): The email address of the contact (maximum length: 50 characters).
          phone (str): The phone number of the contact (maximum length: 15 characters).
          born_date (datetime): The birth date of the contact.
          additional (str): Additional information about the contact (maximum length: 200 characters).
          user_id (int): The foreign key referencing the user to whom the contact belongs.
          user (relationship): Relationship to the User model, representing the owner of the contact.

      Table Name:
          contacts
      """
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    phone = Column(String(15), nullable=False)
    born_date = Column(DateTime)
    additional = Column(String(200))
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", backref="contacts")


class User(Base):
    """
      Database model representing a user.

      This class defines the structure of the 'users' table in the database,
      including various attributes such as id, email, password, refresh_token, and confirmed.

      Attributes:
          id (int): The primary key of the user.
          email (str): The email address of the user (maximum length: 150 characters), unique.
          password (str): The hashed password of the user (maximum length: 255 characters).
          refresh_token (str): The refresh token of the user (maximum length: 255 characters), nullable.
          confirmed (bool): A boolean flag indicating whether the user's email is confirmed.

      Table Name:
          users
      """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
