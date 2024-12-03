from sqlalchemy.orm import Session
from src.database.model import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user


async def create_user(body: UserModel, db: Session) -> User:

    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()
