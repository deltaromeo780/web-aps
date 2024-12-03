from pydantic import BaseModel, Field, EmailStr, PastDate


class ContactBase(BaseModel):
    # id = Column(Integer, primary_key=True)
    # first_name = Column(String(50), nullable=False)
    # last_name = Column(String(50), nullable=False)
    # email = Column(String(50), nullable=False)
    # phone = Column(String(15), nullable=False)
    # born_date = Column(DateTime)
    # additional = Column(String(200), nullable=True)

    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr
    phone: str = Field(max_length=15)
    born_date: PastDate
    additional: str = Field(max_length=200)


class ContactResponse(ContactBase):
    id: int

    class Config:
        # orm_mode = True
        from_attributes = True


class UserModel(BaseModel):
    # __tablename__ = "users"
    # id = Column(Integer, primary_key=True)
    # email = Column(String(150), nullable=False, unique=True)
    # password = Column(String(255), nullable=False)
    # refresh_token = Column(String(255), nullable=True)

    email: str = EmailStr
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
