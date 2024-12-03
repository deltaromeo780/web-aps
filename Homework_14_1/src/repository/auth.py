from sqlalchemy.orm import Session
from src.database.model import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session):
    """
        Asynchronous function to retrieve a user by email from the database.

        This function queries the database session to retrieve a user with the provided email
        address.

        Args:
            email (str): The email address of the user to retrieve.
            db (Session): The database session to perform the query on.

        Returns:
            User: The user object retrieved from the database with the specified email address,
            or None if no user is found.

        Example:
            To retrieve a user with the email address "example@example.com" from the database:
            user = await get_user_by_email("example@example.com", db)
        """
    print("We are in repo.auth.get_user_by_email")

    user = db.query(User).filter(User.email == email).first()
    return user


async def create_user(body: UserModel, db: Session) -> User:
    """
        Asynchronous function to create a new user in the database.

        This function creates a new user in the database using the provided user model object.
        It adds the new user to the database session, commits the transaction, refreshes the
        user object to ensure it reflects the latest state from the database, and then returns
        the newly created user.

        Args:
            body (UserModel): The user model object containing the data for the new user.
            db (Session): The database session to perform the creation operation on.

        Returns:
            User: The newly created user object.

        Example:
            To create a new user with the provided user model data in the database:
            new_user = await create_user(user_model_data, db)
        """
    print("We are in repo.auth.create_user")

    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
      Asynchronous function to update the refresh token for a user in the database.

      This function updates the refresh token for the specified user in the database.
      It sets the refresh token to the provided value (or None if no token is provided),
      commits the transaction to save the changes to the database.

      Args:
          user (User): The user object for which to update the refresh token.
          token (str | None): The new refresh token value, or None if no token is provided.
          db (Session): The database session to perform the update operation on.

      Returns:
          None

      Example:
          To update the refresh token for a user with a new token value:
          await update_token(user_object, new_token_value, db)

          To remove the refresh token for a user:
          await update_token(user_object, None, db)
      """
    print("We are in repo.auth.update_token")
    user.refresh_token = token
    db.commit()


async def confirm_email(email: str, db: Session) -> None:
    """
       Asynchronous function to confirm the email address of a user in the database.

       This function retrieves the user with the specified email address from the database,
       sets the 'confirmed' attribute of the user to True, and commits the transaction to
       save the changes to the database.

       Args:
           email (str): The email address of the user to confirm.
           db (Session): The database session to perform the update operation on.

       Returns:
           None

       Example:
           To confirm the email address of a user with a specific email:
           await confirm_email("example@example.com", db)
       """
    print("We are in repo.auth.confirmed_email")
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    """
       Asynchronous function to update the avatar URL for a user in the database.

       This function retrieves the user with the specified email address from the database,
       sets the 'avatar' attribute of the user to the provided URL, and commits the transaction
       to save the changes to the database. It then returns the updated user object.

       Args:
           email (str): The email address of the user whose avatar URL to update.
           url (str): The new avatar URL for the user.
           db (Session): The database session to perform the update operation on.

       Returns:
           User: The updated user object.

       Example:
           To update the avatar URL for a user with a specific email:
           updated_user = await update_avatar("example@example.com", "https://example.com/avatar.jpg", db)
       """
    print("in repo.auth.update_avatar")
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
