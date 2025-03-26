from flask_restful import Resource, Api
from flask import request
from .models import *


api=Api()

class SubjectApi(Resource):

  #Reading data
  def get(self):
    subjects = Subject.query.all()
    subjects_json = []
    for subject in subjects:
      subjects_json.append({"id" : subject.sub_id, "name" : subject.name, "description" : subject.description})
    return subjects_json
  
  #Creating data
  def post(self):
    pass

  #Updating data
  def put(self):
    pass

  #Deleting data
  def delete(self):
    pass

api.add_resource(SubjectApi,"/api/get_subjects")