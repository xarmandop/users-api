import os
from models.user import User
from flask import Flask, json
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
from resources.user import (
    UserDeactivate, 
    UserLogin, 
    UserRegister, 
    UserList, 
    UserApi,
    TokensRefresh
    )
from resources.health import HealthyCheck
from mongoengine.errors import DoesNotExist
from bson import ObjectId
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)

#By default datetime.timedelta(minutes=15)
#app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 0

#app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 0
#Default: datetime.timedelta(days=30)

app.config["JWT_SECRET_KEY"] = os.environ['JWT_SECRET']

#By default, Flask-MongoEngine assumes that the mongod instance is running on localhost on port 27017, 
# and you wish to connect to the database named test.

app.config["MONGODB_SETTINGS"] = {
    'db' : os.environ['MONGODB_DATABSE'], 
    'host': os.environ['MONGODB_HOSTNAME'],
    'port': os.environ['MONGODB_PORT'],
    'username': os.environ['MONGODB_USERNAME'],
    'password': os.environ['MONGODB_PASSWORD']
}

@jwt.expired_token_loader
def expired_token(_jwt_header, jwt_payload ):
    return { "message": f"The token has expired. {jwt_payload['sub']}  "}    

@jwt.user_identity_loader
def add_claims_to_jwt(identity):
    return identity

@jwt.user_lookup_loader
def authorization(_jwt_header, jwt_data):

   
    user_id = ObjectId(jwt_data["sub"])
    try:
        print(User.objects().get(id = user_id))
        return  User.objects().get(id = user_id)
    except DoesNotExist:
        return None

api.add_resource(UserRegister, '/register')
api.add_resource(TokensRefresh, '/refresh')
api.add_resource(UserLogin, '/login')
api.add_resource(UserList, '/user/list')
api.add_resource(UserApi, '/user/<user_id>')
api.add_resource(UserDeactivate, '/user/deactivate/<user_id>')
api.add_resource(HealthyCheck, '/healthz')

if __name__ == '__main__':
    db.init_app(app)
    app.run(host="0.0.0.0", port=5000)
