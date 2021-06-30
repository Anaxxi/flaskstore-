from flask_restful import Resource, reqparse
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
import base64
from flask_jwt_extended import create_access_token
from datetime import timedelta

from app.models import User
from app.extensions import db
from app.services.mail import send_mail

import logging
import secrets


class Login(Resource):

    def get(self):
        if not request.headers.get("Authorization"):
            return {"message": "error, not authorized"}, 400

        basic, code = request.headers["Authorization"].split(" ")
        if not basic.lower() == "basic":
            return {"message": "Authorization malformated"}, 400

        email, password = code.split(":")

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return {"message":"invalid email or password"}, 400

        token = create_access_token({"id": user.id}, expires_delta=timedelta(hours=5))

        return {"access_token": token}


class Register(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", required=True, help="Email Obrigatório")
        parser.add_argument("password", required=True, help="Senha Obrigatória")
        args = parser.parse_args()

        user = User.query.filter_by(email=args.email).first()
        if user:
            return {"message":"error, email already in use"}


        user = User()
        user.email= args.email
        user.password= generate_password_hash(args.password, salt_length=10)

        db.session.add(user)

        try:
            db.session.commit()
            send_mail("Bem vindo ao Flask Store", user.email, "welcome", email=user.email)
            return {"message":"user registered"}, 201

        except Exception as e:
            db.session.rollback()
            logging.critical(str(e))
            return {"message":"error, could not register"}, 500


class ForgetPassword(Resource):
    def post(self):
        parser = reqparse.RequestParser(trim=True)
        parser.add_argument("email", required=True, help="Email required")
        args = parser.parse_args()

        user = User.query.filter_by(email=args.email).first()

        if not user:
            return {"message": "Data not found"}, 400

        password_temp = secrets.token_hex(8)
        user.password = generate_password_hash(password_temp)
        db.session.add(user)
        db.session.commit()

        send_mail("Recuperação de conta", user.email, "forget-password", password_temp=password_temp)
        return {"message":"Email sent"}
