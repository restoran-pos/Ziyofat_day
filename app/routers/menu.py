from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.database import db_dep
from app.models import MenuCategory, MenuItem, MenuItemVariant
from app.schemas import MenuCategoryRead, MenuItemRead, MenuItemVariantRead

router = APIRouter(prefix="/menu", tags=["Menu"])


@router.get("/categories/", response_model=list[MenuCategoryRead])
def get_categories(session: db_dep):
    """Barcha kategoriyalar (sort_order bo'yicha)"""
    return (
        session.execute(select(MenuCategory).order_by(MenuCategory.sort_order))
        .scalars()
        .all()
    )


@router.get("/categories/{category_id}/", response_model=MenuCategoryRead)
def get_category(category_id: int, session: db_dep):
    """Bitta kategoriya"""
    category = session.get(MenuCategory, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Kategoriya topilmadi")
    return category


@router.get("/items/", response_model=list[MenuItemRead])
def get_items(
    session: db_dep,
    category_id: int | None = None,
    is_active: bool = True,
    station: str | None = None,
):
    pass


@router.get("/items/{item_id}/", response_model=MenuItemRead)
def get_item(item_id: int, session: db_dep):
    """Bitta taom — variantlari bilan"""
    item = session.get(MenuItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Taom topilmadi")
    return item


@router.get("/items/{item_id}/variants/", response_model=list[MenuItemVariantRead])
def get_variants(item_id: int, session: db_dep):
    """Taomning variantlari (katta/kichik porsiya va h.k.)"""
    if not session.get(MenuItem, item_id):
        raise HTTPException(status_code=404, detail="Taom topilmadi")
    return (
        session.execute(
            select(MenuItemVariant).where(
                MenuItemVariant.menu_item_id == item_id,
                MenuItemVariant.is_active == True,  # noqa: E712
            )
        )
        .scalars()
        .all()
    )
