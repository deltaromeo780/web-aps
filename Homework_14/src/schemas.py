from pydantic import BaseModel, Field, EmailStr, PastDate


class ContactBase(BaseModel):
    """
      Pydantic model representing the base contact information.

      Attributes:
          first_name (str): The first name of the contact.
          last_name (str): The last name of the contact.
          email (EmailStr): The email address of the contact.
          phone (str): The phone number of the contact.
          born_date (PastDate): The born date of the contact (in the past).
          additional (str): Additional information about the contact.
      """
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr
    phone: str = Field(max_length=15)
    born_date: PastDate
    additional: str = Field(max_length=200)


class ContactResponse(ContactBase):
    """
        Pydantic model representing the response for contact information.

        Inherits:
            ContactBase

        Attributes:
            id (int): The unique identifier of the contact.
        """
    id: int

    class Config:
        from_attributes = True


class UserModel(BaseModel):
    """
     Pydantic model representing user information for sign-up.

     Attributes:
         email (str): The email address of the user.
         password (str): The password of the user.
     """
    email: str = EmailStr
    # email: str = Field(max_length=50)
    password: str = Field(max_length=255)


class UserBase(BaseModel):
    """
      Pydantic model representing the base user information.

      Attributes:
          email (str): The email address of the user.
      """
    email: str = EmailStr

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """
     Pydantic model representing the response for user creation.

     Attributes:
         user (UserBase): The base user information.
         detail (str): Information message indicating successful user creation.
     """
    user: UserBase
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    """
      Pydantic model representing a token.

      Attributes:
          access_token (str): The access token.
          refresh_token (str): The refresh token.
          token_type (str): Type of the token (default is "bearer").
      """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    """
      Pydantic model representing a request for email.

      Attributes:
          email (str): The email address.
      """
    email: str = Field(max_length=50)


class UserDb(BaseModel):
    """
     Pydantic model representing user information retrieved from the database.

     Attributes:
         id (int): The unique identifier of the user.
         email (str): The email address of the user.
         avatar (str, None): The URL of the user's avatar, or None if not available.
     """
    id: int
    email: str
    avatar: str | None

    class Config:
        from_attributes = True


class UserAvatar(BaseModel):
    """
     Pydantic model representing the user's avatar.

     Attributes:
         avatar (str): The URL of the user's avatar.
     """
    avatar: str

    class Config:
        from_attributes = True
