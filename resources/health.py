from flask_restful import Resource
from flask import jsonify
from models.health import Health
from mongoengine.errors import ValidationError, DoesNotExist
from datetime import datetime


_now = datetime.now() 
_current_time = _now.strftime("%m/%d/%Y, %H:%M:%S")

_HEALTH_WORKING_MESSAGE = { "status": f"Application working correctly at: {_current_time}." }
_HEALTH_NOT_WORKING_MESSAGE = { "status": f"Application present issues at: {_current_time}." }


#containers and K8s propouses
class HealthyCheck(Resource):
    
    def get(self):
        try:
            #lastCheck = Health.objects().exclude('id').order_by("checktime").first()
            return _HEALTH_WORKING_MESSAGE

        except (DoesNotExist, ValidationError):
            return _HEALTH_NOT_WORKING_MESSAGE, 500
        

    def post(self):
        try:
            Health(status = _HEALTH_WORKING_MESSAGE).save()
            return _HEALTH_WORKING_MESSAGE, 200
        
        except ValidationError:
            return _HEALTH_NOT_WORKING_MESSAGE, 500


