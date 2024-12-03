from pydantic import BaseModel, Field, EmailStr, PastDate


class ContactBase(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr
    phone: str = Field(max_length=15)
    born_date: PastDate
    additional: str = Field(max_length=200)


class ContactResponse(ContactBase):
    id: int

    class Config:
        from_attributes = True


class UserModel(BaseModel):
    email: str = EmailStr
    # email: str = Field(max_length=50)
    password: str = Field(max_length=255)


class UserBase(BaseModel):
    email: str = EmailStr

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user: UserBase
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: str = Field(max_length=50)


class UserDb(BaseModel):
    id: int
    email: str
    avatar: str | None

    class Config:
        from_attributes = True


class UserAvatar(BaseModel):
    avatar: str

    class Config:
        from_attributes = True
