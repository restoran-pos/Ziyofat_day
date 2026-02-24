from fastapi import FastAPI
from app.routers import table_router

app=FastAPI(
    title="ZIYOFAT-DAY"
)

app.include_router(table_router)