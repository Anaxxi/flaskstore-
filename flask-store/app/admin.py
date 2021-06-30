from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from slugify import slugify
from wtforms.fields import StringField
from wtforms.validators import Optional
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models import User, Product, Category, Profile, Order, Item


class UserModel(ModelView):
    inline_models =[Profile]

    def on_model_change(self, form, model, is_created):
        model.password = generate_password_hash(form.password.data, salt_length=10)

class CategoryModel(ModelView):

    form_extra_fields = {
        "slug": StringField("slug", validators=[Optional()])
    }

    def on_model_change(self, form, model, is_created):
        model.slug = slugify(form.name.data)
        return

class ProductModel(ModelView):
    form_extra_fields = {
        "slug": StringField("slug", validators=[Optional()])
    }

    column_searchable_list = ("name", )
    column_sortable_list = ("name", "price", "quantity")
    column_filters = ("price", "quantity")

    def on_model_change(self, form, model, is_created):
        model.slug = slugify(form.name.data)
        return

class ItemModel(ModelView):
    column_searchable_list = ("order_id", )

    #def on_model_change(self, form, model, is_created):

def init_app(app):
    admin = Admin(app, name="FLASK STORE")
    admin.add_view(UserModel(User, db.session))
    admin.add_view(ModelView(Profile, db.session))
    admin.add_view(ProductModel(Product, db.session))
    admin.add_view(CategoryModel(Category, db.session))
    admin.add_view(ItemModel(Item, db.session))
    admin.add_view(ModelView(Order, db.session))
