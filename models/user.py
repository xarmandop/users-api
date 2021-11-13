from db import db

#Rol :
#  0 = admin
#  1 = basic  

class User(db.Document):
    email = db.StringField(max_length=500, required=True)
    password = db.StringField(max_lenght=250, required=True)
    role = db.IntField(min_value=0, max_value=1, required=True)
    activate = db.BooleanField(default=True)