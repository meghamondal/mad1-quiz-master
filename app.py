from flask import Flask
from backend.config import LocalDevelopmentConfig
from backend.models import db
from backend.api_controllers import *

app = None

def create_app():
  app = Flask(__name__)
  app.config.from_object(LocalDevelopmentConfig)
  db.init_app(app) # Flask app is connected to db
  api.init_app(app)# Flask app is connected to apis
  app.app_context().push() # Direct access to other modules

  return app

app = create_app()

import backend.initial_data
import backend.controllers



if __name__ == '__main__':
  app.run(port=8080, debug=True)
