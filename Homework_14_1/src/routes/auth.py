from fastapi import (
    APIRouter, HTTPException, Depends, status, Security, BackgroundTasks, Request)

from fastapi.security import (
    OAuth2PasswordRequestForm,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import UserModel, UserResponse, TokenModel, RequestEmail
from src.repository import auth as repository_users
from src.services.auth import auth_service
from src.services.email import send_email

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel, background_tasks: BackgroundTasks, request: Request,
                 db: Session = Depends(get_db)):
    """
        Endpoint to sign up a new user.

        This route handles the sign-up process for new users. It first checks if the provided email
        already exists in the database. If the email is not found, a new user is created with the
        provided details. A confirmation email is sent to the user's email address asynchronously.

        Args:
            body (UserModel): The user model object containing sign-up data.
            background_tasks (BackgroundTasks): Background tasks to run asynchronously.
            request (Request): The request object.
            db (Session, optional): The database session. Defaults to Depends(get_db).

        Returns:
            UserResponse: The response containing the newly created user and a success message.

        Raises:
            HTTPException: If the provided email already exists in the database.
        """
    print("We are in routes.auth.signup")
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    background_tasks.add_task(send_email, new_user.email, request.base_url)
    return {"user": new_user, "detail": "User successfully created. Check your email for confirmation."}


@router.post("/login", response_model=TokenModel)
async def login(
        body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
       Endpoint to log in a user.

       This route handles user authentication by verifying the provided email and password.
       If the email exists in the database and the password matches, a token pair (access token
       and refresh token) is generated and returned to the client for authentication.

       Args:
           body (OAuth2PasswordRequestForm): The form containing the user's email and password.
           db (Session): The database session. Defaults to Depends(get_db).

       Returns:
           TokenModel: The response containing the access token, refresh token, and token type.

       Raises:
           HTTPException: If the provided email is invalid or not found in the database,
           or if the password is incorrect.
       """

    print("We are in routes.auth.login")
    user = await repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email"
        )

    #    if not user.confirmed:
    #        raise HTTPException(
    #            status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed"
    #        )

    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )
    # Generate JWT
    access_token = await auth_service.create_token(
        data={"sub": user.email}, token_type="access_token"
    )
    refresh_token = await auth_service.create_token(
        data={"sub": user.email}, token_type="refresh_token"
    )
    await repository_users.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/refresh_token", response_model=TokenModel)
async def refresh_token(
        credentials: HTTPAuthorizationCredentials = Security(security),
        db: Session = Depends(get_db),
):
    """
       Endpoint to refresh an access token using a refresh token.

       This route allows users to refresh their access token using a valid refresh token.
       It decodes the provided refresh token to extract the user's email, verifies the refresh
       token against the user's stored refresh token in the database, and generates a new pair
       of access token and refresh token. The new refresh token is then stored in the database.

       Args:
           credentials (HTTPAuthorizationCredentials): The HTTP authorization credentials containing the refresh token.
           db (Session): The database session. Defaults to Depends(get_db).

       Returns:
           TokenModel: The response containing the new access token, new refresh token, and token type.

       Raises:
           HTTPException: If the refresh token is invalid or does not match the one stored in the database.
       """
    print("We are in routes.auth.refresh_token")
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    access_token = await auth_service.create_token(
        data={"sub": email}, token_type="access_token"
    )
    refresh_token = await auth_service.create_token(
        data={"sub": email}, token_type="refresh_token"
    )
    await repository_users.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    """
        Endpoint to confirm a user's email address using a confirmation token.

        This route verifies the email confirmation token provided in the URL. It decodes the token
        to extract the user's email address and confirms the email address in the database. If the
        email address is successfully confirmed, a success message is returned.

        Args:
            token (str): The email confirmation token.
            db (Session): The database session. Defaults to Depends(get_db).

        Returns:
            dict: A message indicating the status of the email confirmation.

        Raises:
            HTTPException: If the email confirmation token is invalid or if there's an error during verification.
        """
    print("We are in routes.auth.confirmed_email")
    email = await auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await repository_users.confirm_email(email, db)
    return {"message": "Email confirmed"}


@router.post("/request_email")
async def request_email(
        body: RequestEmail,
        background_tasks: BackgroundTasks,
        request: Request,
        db: Session = Depends(get_db),
):
    """
        Endpoint to request email confirmation.

        This route sends an email to the user's provided email address with a confirmation link
        to confirm their email address. If the email address is already confirmed, it returns
        a message indicating that the email is already confirmed.

        Args:
            body (RequestEmail): The request body containing the user's email address.
            background_tasks (BackgroundTasks): Background tasks to run asynchronously.
            request (Request): The request object.
            db (Session): The database session. Defaults to Depends(get_db).

        Returns:
            dict: A message indicating the status of the email confirmation request.

        Raises:
            HTTPException: If there's an error during the email confirmation request.
        """
    print("We are in routes.auth.request_email")
    user = await repository_users.get_user_by_email(body.email, db)

    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(send_email, user.email, user.email, request.base_url)
    return {"message": "Check your email for confirmation."}
