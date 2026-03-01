import os
from fastapi import APIRouter, Request, UploadFile, Form, File


from app.schemas import UserProfileResponse
from app.dependencies import current_user

router = APIRouter(prefix="/user", tags=["User"])


def _safe_ext(filename: str) -> str:
    _, ext = os.path.splitext(filename or "")
    return ext.lower()[:10] if ext else ""  # TODO: move to UTILS


UPLOAD_DIR = "media_uploads"  # TODO: config settings


@router.get("/profile/", response_model=UserProfileResponse)
async def me(current_user: current_user):
    return UserProfileResponse(
        username=current_user.username,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        avatar_url=(current_user.avatar.url if current_user.avatar else None),
    )


@router.put("/profile/update", response_model=UserProfileResponse)
async def update_me(
    current_user: current_user,
    request: Request,
    first_name: str | None = Form(None),
    last_name: str | None = Form(None),
    avatar: UploadFile | None = File(None),
):
    pass


@router.post("/avatar/upload/", response_model=UserProfileResponse)
async def upload_avatar(
    current_user: current_user,
    request: Request,
    avatar: UploadFile | None = File(None),
):
    pass


@router.delete("/avatar/delete/", response_model=UserProfileResponse)
async def delete_avatar(
    current_user: current_user,
    request: Request,
):
    pass
