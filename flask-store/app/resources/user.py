from flask_restful import Resource, marshal, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models import User, Profile
from app.schemas import user_items_fields, profile_fields
from app.extensions import db
import logging



class Orders(Resource):

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.get(current_user["id"])
        return marshal(user.item, user_items_fields, "order")


class UpdateProfile(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.get(current_user["id"])
        return marshal(user.profile, profile_fields, "profile")

    @jwt_required()
    def put(self):

        parser = reqparse.RequestParser(trim=True)
        parser.add_argument("first_name", required=True)
        parser.add_argument("last_name", required=True)
        parser.add_argument("document", required=True)
        parser.add_argument("phone", required=True)
        args = parser.parse_args(strict=True)

        current_user = get_jwt_identity()
        user = User.query.get(current_user["id"])
        if not user.profile:
            user.profile = Profile()

        user.profile.first_name = args.first_name
        user.profile.last_name = args.last_name
        user.profile.document = args.document
        user.profile.phone = args.phone

        try:
            db.session.commit()
            return marshal(user.profile, profile_fields, "profile")

        except Exception as e:
            logging.error(str(e))
            db.session.rollback()
            return {"message":"Error, try again later"}, 500
