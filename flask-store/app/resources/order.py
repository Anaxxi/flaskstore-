from flask_restful import Resource, reqparse, marshal
from flask import current_app
from random import getrandbits
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime
import logging

from app.models import Product, Order, Item, Category
from app.extensions import db
from app.schemas import order_fields, create_product_fields, category_fields, create_product_fields_att
#from app.services.picpay import picpay

class CreateProduct(Resource):
    @jwt_required()
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("slug", type=str, required=True)
        parser.add_argument("price", type=float, required=True)
        #parser.add_argument("image", type=str, required=True)
        parser.add_argument("quantity", type=int, required=True)
        parser.add_argument("description", type=str, required=False)
        args = parser.parse_args()

        exist = Product.query.filter_by(slug=args.slug).first()
        if exist:
            return {"message": "Product already exists"}, 500

        product = Product()
        product.name = args.name
        product.slug = args.slug
        product.price = args.price
        #product.image = args.image,
        product.quantity = args.quantity
        product.description = args.description



        try:
            db.session.add(product)
            db.session.commit()
            return marshal(product, create_product_fields, "product"), 201


        except Exception as e:
            logging.critical(str(e))
            db.session.rollback()
            return {"message":"Couldn't create Product"}, 500

    
class CreateCategory(Resource):
    @jwt_required()
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("slug", type=str, required=True)
        args = parser.parse_args()


        category = Category()
        category.name = args.name
        category.slug = args.slug

        try:
            db.session.add(category)
            db.session.commit()
            return marshal(category, category_fields, "category"), 201

        except Exception as e:
            logging.critical(str(e))
            db.session.rollback()
            return {"message":"Couldn't create Category or it already exists"}, 500






class Create(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument("product_id", type=int, required=True, help="product_id Required")
        parser.add_argument("quantity", type=int, required=True, help="quantity Required")
        args = parser.parse_args()

        product = Product.query.get(args.product_id)
        if not product:
            return {"message": "out of product"}, 400

        if args.quantity > product.quantity:
            return {"message":"we're out of that quantity"}, 400

        try:
            order=Order()
            order.reference_id = f"FLKST-{getrandbits(16)}"
            db.session.add(order)
            db.session.commit()

            item = Item()
            item.order_id = order.id
            item.product_id = args.product_id
            item.user_id = current_user["id"]
            item.quantity = args.quantity
            item.price = product.price * args.quantity
            db.session.add(item)
            db.session.commit()
            return marshal(order, order_fields, "order")

        except Exception as e:
            logging.critical(str(e))
            db.session.rollback()
            return {"message":"couldn't create order"}, 500


class Pay(Resource):
    pass
    #@jwt_required()
    #def get(self):
    #    order = Order.query.filter_by(reference_id=reference_id_).first()
    #    if not order:
    #        return {"message": "Order doesn't exist"}, 400


    #    expires = datetime.datime.now() + datetime.timedelta(days=3)

        #response = picpay.payment(
        #    {
        #        "referenceId": order.reference_id,
        #        "callbackUrl": current_app.config["PICPAY_CALLBACK_URL"],
        #        "returnUrl": current_app.config["PICPAY_RETURN_URL"],
        #        "value": order.item.price,
        #        "expiresAt": expires.isoformat(),
        #        "channel": "my-channel",
        #        "purchaseMode": "in-store",
        #        "buyer": {
        #            "firstName": order.item.user.profile.first_name,
        #            "lastName": order.item.user.profile.last_name,
        #            "document": order.item.user.profile.document,
        #            "email": order.item.user.email,
        #            "phone": order.item.user.profile.phone
        #            }
        #    }
        #)
        #return response.json()


class Notification(Resource):
    pass
