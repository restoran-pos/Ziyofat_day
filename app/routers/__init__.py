from .dining_table import router as table_router
from .auth.login import router as login_router

__all__ = [
    table_router,
    login_router
           ]
