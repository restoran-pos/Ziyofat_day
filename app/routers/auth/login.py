import os
from datetime import datetime, timezone, timedelta
import uuid

from fastapi import APIRouter, HTTPException,UploadFile,Depends,Form,Request,File
from sqlalchemy import select

from app.database import db_dep,get_db
from app.dependencies import current_user
from app.schemas import UserLoginRequest, RefreshTokenRequest, UserProfileResponse
from app.models import User,Media,TokenBlacklist
from app.utils import verify_password, generate_jwt_tokens, decode_jwt_token

def _safe_ext(filename: str) -> str:
    _, ext = os.path.splitext(filename or "")
    return (ext.lower()[:10] if ext else "")


UPLOAD_DIR = "media_uploads"  

router = APIRouter(prefix="/auth", tags=["Auth"])


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

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

jwt_security = HTTPBearer(auto_error=False)

@router.post("/logout", status_code=200)
async def logout(
    session:db_dep,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(jwt_security),
):
    if not credentials:
        raise HTTPException(status_code=401, detail="Invalid token")

    token = credentials.credentials  # toza token

    session.add(TokenBlacklist(token=token))
    session.commit()

    return {"detail": "Logout successfully"}