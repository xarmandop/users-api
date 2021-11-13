from db import db
from datetime import datetime

#Working/not working logs
#For a better approach implement metrics
class Log(db.Document):
    ipClient = db.StringField(max_length=50, required=True)
    uriRequested = db.StringField(max_length=100, required=True)
    httpCode = db.IntField(required=True)
    exception = db.StringField(max_length=1500, required=True)
    datetime = db.DateTimeField(default=datetime.utcnow, required=True)


