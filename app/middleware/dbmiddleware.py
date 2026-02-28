from starlette.middleware.base import BaseHTTPMiddleware
from app.database import SessionLocal,get_db

class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request.state.session = SessionLocal()
        try:
            response = await call_next(request)
            request.state.session.commit()
            return response
        except:
            request.state.session.rollback()
            raise
        finally:
            request.state.session.close()