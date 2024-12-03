from sqlalchemy.orm import Session
from src.database.model import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session):
    print("We are in repo.auth.get_user_by_email")

    user = db.query(User).filter(User.email == email).first()
    return user


async def create_user(body: UserModel, db: Session) -> User:
    print("We are in repo.auth.create_user")

    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    print("We are in repo.auth.update_token")
    user.refresh_token = token
    db.commit()


async def confirm_email(email: str, db: Session) -> None:
    print("We are in repo.auth.confirmed_email")
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    print("in repo.auth.update_avatar")
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
