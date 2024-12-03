from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from src.database.db import get_db
from src.database.model import User
from src.repository import auth as repository_users
from src.services.auth import auth_service
from src.conf.config import settings
from src.schemas import UserDb, UserAvatar

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserDb)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
      Endpoint to retrieve the details of the current authenticated user.

      This route retrieves the details of the current authenticated user based on the access token
      provided. It returns information such as the user's ID, email, and other attributes.

      Args:
          current_user (User): The current authenticated user obtained from the access token.

      Returns:
          UserDb: The details of the current authenticated user.

      Raises:
          HTTPException: If there's an error during the retrieval of the user details.
      """
    print("in routes.users.read_users_me")
    return current_user


@router.patch("/avatar", response_model=UserAvatar)
async def update_avatar_user(
    file: UploadFile = File(),
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
       Endpoint to update the avatar of the current authenticated user.

       This route allows the current authenticated user to update their avatar image. It expects
       a file upload containing the new avatar image. Upon successful upload, the route updates
       the avatar URL in the database and returns the updated user object with the new avatar URL.

       Args:
           file (UploadFile): The file containing the new avatar image to be uploaded.
           current_user (User): The current authenticated user obtained from the access token.
           db (Session): The database session. Defaults to Depends(get_db).

       Returns:
           UserAvatar: The updated user object containing the new avatar URL.

       Raises:
           HTTPException: If there's an error during the upload of the new avatar image
                          or during the update of the avatar URL in the database.
       """
    print("in routes.users.update_avatar_user")
    cloudinary.config(
        cloud_name=settings.cloud_name,
        api_key=settings.api_key,
        api_secret=settings.api_secret,
        secure=True,
    )

    r = cloudinary.uploader.upload(
        file.file, public_id=f"ContactsApp/{current_user.email}", overwrite=True
    )
    src_url = cloudinary.CloudinaryImage(f"ContactsApp/{current_user.email}").build_url(
        width=250, height=250, crop="fill", version=r.get("version")
    )
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user
