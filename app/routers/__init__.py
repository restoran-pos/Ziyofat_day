from .dining_table import router as table_router
from .auth.login import router as login_router
from .menu import router as menu_router
from .order import router as order_router
from .user import router  as user_router

__all__ = [
    table_router,
    login_router,
    menu_router,
    order_router
           ]
