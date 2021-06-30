from flask_restful import fields


category_fields = {
    "name":fields.String,
    "slug":fields.String
}

product_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "slug": fields.String,
    "price": fields.Float,
    "quantity": fields.Integer,
    "categories": fields.List(fields.Nested(category_fields))
    }


item_fields = {
    "quantity": fields.Integer,
    "price": fields.Float,
}

order_fields = {
    "reference_id": fields.String,
    "items": fields.Nested(item_fields),
    "status": fields.String
}

user_orders_fields = {
    "reference_id": fields.String,
    "status": fields.String
}

user_items_fields = {
    "quantity": fields.Integer,
    "price": fields.Float,
    "order": fields.Nested(user_orders_fields),
    "product": fields.Nested(product_fields)
}

create_product_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "slug": fields.String,
    "price": fields.Float,
    #"image": fields.String,
    "quantity": fields.Integer,
    "description": fields.String,
    "created_at": fields.String
}
create_product_fields_att = {
    "name": fields.String,
    "price": fields.Float,
    #"image": fields.String,
    "quantity": fields.Integer,
    "description": fields.String
}

profile_fields = {
    "first_name":fields.String,
    "last_name":fields.String,
    "document":fields.String,
    "phone":fields.String
}

register_fields = {
"email": fields.String}