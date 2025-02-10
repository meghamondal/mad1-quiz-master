from flask import Flask
from backend.config import LocalDevelopmentConfig
from backend.models import db

app = None

def create_app():
  app = Flask(__name__)
  app.config.from_object(LocalDevelopmentConfig)
  db.init_app(app)
  app.app_context().push()

  return app

app = create_app()

import backend.initial_data
import backend.controllers


if __name__ == '__main__':
  app.run(port=8080, debug=True)
