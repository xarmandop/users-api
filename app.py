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

#This most be set as Variable environment and get
#'import os; print(os.urandom(16))'
app.config["JWT_SECRET_KEY"] = "super-secret-xarmandop"

#By default datetime.timedelta(minutes=15)
#app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 0

#app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 0
#Default: datetime.timedelta(days=30)

app.config['MONGODB_SETTINGS'] = {
    "db" : 'next_tattoo',
    'host' : 'localhost',
    'port' : 27017
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
    app.run(debug=True)
