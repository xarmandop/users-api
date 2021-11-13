import datetime
import argon2
from flask_restful import Resource, reqparse, request
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    jwt_required, 
    current_user
    )
from flask import jsonify
from argon2.exceptions import VerifyMismatchError
from models.user import User
from models.log import Log
from bson.objectid import ObjectId
from bson.errors import InvalidId
from mongoengine.errors import ValidationError, DoesNotExist
from flask import request
import tags
from datetime import timedelta 


_ph = argon2.PasswordHasher()
_user_parser = reqparse.RequestParser()

_user_parser.add_argument(
    'email',
    type = str,
    required = True,
    help = tags.FIELD_NOT_BLANK
)

_user_parser.add_argument(
    'password',
    type = str,
    required = True,
    help = tags.FIELD_NOT_BLANK
)

_user_parser.add_argument(
    'role',
    type = int,
    required = True,
    help = tags.FIELD_NOT_BLANK
)


class UserRegister(Resource): 

    def post(self):
        data = _user_parser.parse_args()
        user =  User.objects(email = data["email"]).first()

        if not user:
            data.password = _ph.hash(data["password"])
            user = User(**data)
        
            try: 
                user.save()
                return tags.SUCCESS , 201
            except ValidationError:
                return tags.ERROR_SAVING_USR , 500
        else: 
            return tags.USR_ALREADY_EXIST, 400



class UserApi(Resource):

    def get(self, user_id):
        try:
            user = User.objects().exclude("password").get(id = ObjectId(user_id))    
            return jsonify( user ) 
        except DoesNotExist: 
            return tags.USR_NOT_EXISTS, 401

    @jwt_required(fresh=True)
    def delete(self, user_id):
        
        if current_user.role == 0 and current_user.id is not user_id:
            try:
                User.objects().get(id = ObjectId(user_id)).delete()
            except DoesNotExist:
                return tags.USR_NOT_EXISTS, 404
        else:
            return tags.REQUIRE_ADMIN_PRIV, 401



class UserList(Resource):
       
    @jwt_required()
    def get(self): 

        try:
            users = User.objects().exclude("password").order_by("-activate")
            return jsonify(users)
        except:
            return tags.ERROR_SAVING_USR, 500



class UserLogin(Resource):

    def post(self):
        data = _user_parser.parse_args()
        
        try:
            user = User.objects().get(email = data["email"])

            if user.activate and _ph.verify(user.password, data["password"]):
                access_token = create_access_token(identity= str(user.id), fresh= datetime.timedelta(minutes=5))
                refresh_acess_token = create_refresh_token(identity=str(user.id))
                return { "access_token": access_token, "refresh_token": refresh_acess_token }
            else:
                return tags.USR_UNACTIVATED, 401

        except VerifyMismatchError:
                return  tags.CREDENTIALS_INCORRECT, 401
        
        except DoesNotExist:
                return tags.USR_NOT_EXISTS, 401



class UserDeactivate(Resource):
    
    @jwt_required(fresh=True)
    def put(self, user_id):
        
        if current_user.role == 0 and current_user.id is not user_id:
            try:
                usr = User.objects().get(id=ObjectId(user_id)).modify(activate=False)
                usr.reload()
                    
            except (DoesNotExist, InvalidId):
                return tags.ERROR_ID , 500
        else:

            return tags.REQUIRE_ADMIN_PRIV, 401



class TokensRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        new_token = create_access_token(identity= str(current_user.id), fresh=False)
        return {'access_token': new_token}, 200