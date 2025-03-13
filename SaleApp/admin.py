from flask import redirect
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from models import Category, Product, UserEnum
from SaleApp import app, db
from flask_login import logout_user, current_user


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserEnum.ADMIN


class MyCategoryView(AuthenticatedView):
    column_list = ['id', 'name', 'products']
    column_filters = ['name']
    column_searchable_list = ['name']
    can_export = True

class MyProductView(AuthenticatedView):
    column_list = ['id', 'name', 'price', 'cate_id']
    column_filters = ['name']
    column_searchable_list = ['name']
    can_export = True


class LogoutAdmin(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('/admin/stats.html')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserEnum.ADMIN

admin = Admin(app=app, name="E-COMMERCE", template_mode="bootstrap4")

admin.add_view(MyCategoryView(Category, db.session))
admin.add_view(MyProductView(Product, db.session))

admin.add_view(StatsView(name="Thống kê"))
admin.add_view(LogoutAdmin(name="Đăng xuất"))