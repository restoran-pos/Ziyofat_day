from starlette_admin.contrib.sqla import Admin

from app.database import engine
from app.models import User,MenuCategory,MenuItem
from .views import UserAdminView,MenuCategoryView,MenuItemView

admin = Admin(engine=engine, title="ZIYOFAT ADMIN", base_url="/admin")

admin.add_view(UserAdminView(User, icon="fa fa-user"))
admin.add_view(MenuCategoryView(MenuCategory,icon="fa fa-list"))
admin.add_view(MenuItemView(MenuItem,icon="fa fa-utensils"))