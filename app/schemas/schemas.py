from pydantic import BaseModel


class TableBase(BaseModel):
    table_no: str
    capacity: int
    status: str


class TableCreate(TableBase):
    pass  # Admin CRUD uchun kerak bo‘lsa


class TableRead(TableBase):
    id: int


class UserProfileResponse(BaseModel):
    username: str |None =None
    first_name:str | None = None
    last_name:str | None = None
    avatar_url:str | None = None
    
    
class UserLoginRequest(BaseModel):
    username:str | None = None
    password:str | None = None
    
    
class RefreshTokenRequest(BaseModel):
    refresh_token: str
    
    
class UserUploadRequest(BaseModel):
    pass