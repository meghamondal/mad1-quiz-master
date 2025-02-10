class Config():
  DEBUG = False
  SQL_ALCHEMY_TRACK_MODIFICATIONS = False 

class LocalDevelopmentConfig(Config):
  SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3"
  DEBUG=True
  SECRET_KEY = "flaskisasceret"
