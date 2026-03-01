from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import (
    table_router,
    login_router,
    menu_router,
    order_router,
    user_router
    )
# from app.middleware.dbmiddleware import DBSessionMiddleware
from app.admin.settings import  admin
app = FastAPI(title="ZIYOFAT-DAY")


app.include_router(login_router)
app.include_router(user_router)
app.include_router(table_router)
app.include_router(menu_router)
app.include_router(order_router)

# app.add_middleware(DBSessionMiddleware)

admin.mount_to(app=app)


app.mount("/static/uploads", StaticFiles(directory="media_uploads"), name="uploads")