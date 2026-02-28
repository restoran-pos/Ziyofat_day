import os
from datetime import datetime, timezone, timedelta
import uuid

from fastapi import APIRouter, HTTPException,UploadFile,Depends,Form,Request,File
from sqlalchemy import select

from app.database import db_dep,get_db
from app.dependencies import current_user
from app.schemas import UserLoginRequest, RefreshTokenRequest, UserProfileResponse
from app.models import User,Media
from app.utils import verify_password, generate_jwt_tokens, decode_jwt_token

def _safe_ext(filename: str) -> str:
    _, ext = os.path.splitext(filename or "")
    return (ext.lower()[:10] if ext else "")


UPLOAD_DIR = "media_uploads"  

router = APIRouter(prefix="/jwt", tags=["Auth"])


@router.post("/login/")
async def login(db: db_dep, 
                username:str|None = Form(None),
                password:str|None = Form(None)):
    # email, password ask
    # user topilsa, yangi access va refresh tokenlar generatsiya qilamiz
    stmt = select(User).where(User.username == username)
    user = db.execute(stmt).scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token, refresh_token = generate_jwt_tokens(user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@router.post("/refresh/")
async def refresh(db: db_dep, data: RefreshTokenRequest):
    decoded_data = decode_jwt_token(data.refresh_token)

    exp_time = datetime.fromtimestamp(decoded_data["exp"], tz=timezone.utc)
    if exp_time < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Refresh token expired. Please log in.")
    
    user_id = decoded_data["sub"]
    access_token = generate_jwt_tokens(user_id, is_access_only=True)

    return {
        "access_token": access_token,
    }


@router.get("/me/", response_model=UserProfileResponse)
async def me(current_user: current_user):
    return UserProfileResponse(
        username=current_user.username,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        avatar_url=(current_user.avatar.url if current_user.avatar else None),
    )
    
    
@router.patch("/update",response_model=UserProfileResponse)
async def update_me(
    current_user:current_user,
    request: Request,
    first_name: str | None = Form(None),
    last_name: str | None = Form(None),
    avatar: UploadFile | None = File(None)
):
    session = request.state.session

    current_user = session.merge(current_user)
    if first_name is not None:
        current_user.first_name = first_name
    if last_name is not None:
        current_user.last_name = last_name

    if avatar:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        filename = f"{uuid.uuid4().hex}{_safe_ext(avatar.filename)}"
        path = os.path.join(UPLOAD_DIR, filename)

        with open(path, "wb") as f:
            f.write(await avatar.read())

        media = Media(url=f"/static/uploads/{filename}")
        session.add(media)
        session.flush([media])

        current_user.avatar_id = media.id

    session.commit()
    session.refresh(current_user)
    
    return current_user