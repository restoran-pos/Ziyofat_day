from datetime import datetime,timezone
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from fastapi import HTTPException,Depends
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from app.database import db_dep
from app.models import User,TokenBlacklist
from app.utils import decode_jwt_token



jwt_security=HTTPBearer(auto_error=False)
def get_current_user_jwt(session: db_dep, credentials: HTTPAuthorizationCredentials = Depends(jwt_security)):
    if not credentials:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token=credentials.credentials
    stmt = select(TokenBlacklist).where(TokenBlacklist.token == token)
    if session.execute(stmt).scalar():
        raise HTTPException(status_code=401, detail="Token in blacklist")

    
    decoded = decode_jwt_token(credentials.credentials)
    user_id = decoded["sub"]
    exp = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)

    if exp < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Token expired.")

    stmt = (
        select(User)
        .where(User.id == user_id)
        .options(
        joinedload(User.avatar))
    )
    user = session.execute(stmt).scalars().first()

    if not user or user.is_deleted:
        raise HTTPException(status_code=404, detail="User not found")

    return user


current_user= Annotated[User, Depends(get_current_user_jwt)]