from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.repository import auth as repository_users
from src.conf.config import settings

import redis


class Auth:
    """
        Authentication service class responsible for user authentication and token generation.

        This class provides methods for user authentication, password hashing, token generation,
        decoding refresh tokens, retrieving the current authenticated user, and generating email tokens.

        Attributes:
            pwd_context (CryptContext): Password hashing context using bcrypt algorithm.
            SECRET_KEY (str): Secret key used for token encoding and decoding.
            ALGORITHM (str): Algorithm used for token encoding and decoding.
            oauth2_scheme (OAuth2PasswordBearer): OAuth2 password bearer scheme.
            r (Redis): Redis connection object for token storage.
        """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
    r = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)

    def verify_password(self, plain_password, hashed_password):
        """
              Verify the provided plain password against the hashed password.

              Args:
                  plain_password (str): The plain password to verify.
                  hashed_password (str): The hashed password to compare against.

              Returns:
                  bool: True if the passwords match, False otherwise.
              """
        print("We are in Auth.verify_password")
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        """
               Generate a hashed version of the provided password.

               Args:
                   password (str): The password to hash.

               Returns:
                   str: The hashed password.
               """
        print("We are in Auth.get_password_hash")
        return self.pwd_context.hash(password)

    # define a function to generate a new token access/refresh
    async def create_token(self, data: dict, token_type: str):
        """
               Generate a new JWT token.

               Args:
                   data (dict): The data to encode into the token.
                   token_type (str): The type of token to generate.

               Returns:
                   str: The encoded JWT token.
               """
        print("We are in Auth.create_token")
        to_encode = data.copy()

        if token_type == "access_token":
            expire = datetime.utcnow() + timedelta(minutes=15)
        elif token_type == "refresh_token":
            #       elif token_type in ["refresh_token", "email_token"]:
            expire = datetime.utcnow() + timedelta(days=7)
        else:
            raise NameError("Given token_type is not available")

        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": token_type})
        encoded_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_token

    async def decode_refresh_token(self, refresh_token: str):
        """
                Decode and verify a refresh token.

                Args:
                    refresh_token (str): The refresh token to decode.

                Returns:
                    str: The email associated with the refresh token.

                Raises:
                    HTTPException: If the token cannot be decoded or if the scope is invalid.
                """
        print("We are in Auth.decode_refresh_token")
        try:
            payload = jwt.decode(
                refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM]
            )
            if payload["scope"] == "refresh_token":
                email = payload["sub"]
                return email
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid scope for token",
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

    async def get_current_user(
            self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
    ):
        """
               Retrieve the current authenticated user.

               Args:
                   token (str): The JWT token obtained from the request.
                   db (Session): The database session.

               Returns:
                   User: The current authenticated user.

               Raises:
                   HTTPException: If the token cannot be decoded or if the user cannot be retrieved.
               """
        print("We are in Auth.get_current_user")
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            # Decode JWT
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload["scope"] == "access_token":
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            raise credentials_exception

        user = await repository_users.get_user_by_email(email, db)
        if user is None:
            raise credentials_exception
        return user

    def create_email_token(self, data: dict):
        """
             Generate a new email verification token.

             Args:
                 data (dict): The data to encode into the token.

             Returns:
                 str: The encoded email verification token.
             """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token

    async def get_email_from_token(self, token: str):
        """
               Decode an email verification token.

               Args:
                   token (str): The email verification token to decode.

               Returns:
                   str: The email associated with the token.

               Raises:
                   HTTPException: If the token cannot be decoded or if it's invalid.
               """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email = payload["sub"]
            return email
        except JWTError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Invalid token for email verification")


auth_service = Auth()
