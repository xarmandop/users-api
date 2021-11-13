from db import db
from datetime import datetime

class Health(db.Document):
     status = db.StringField(max_length=100, required=True)
     checktime = db.DateTimeField(default=datetime.utcnow, required=True)