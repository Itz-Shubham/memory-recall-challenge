import os
from dotenv import load_dotenv
load_dotenv()

class BaseConfig():
   API_PREFIX = '/api'
   TESTING = False
   DEBUG = False
   SECRET_KEY = os.environ.get('SECRET_KEY')
   UPLOAD_FOLDER = '/uploads'
   ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
   MAX_CONTENT_LENGTH = 10 * 1000 * 1000
   MAIL_SERVER = 'smtp.sendgrid.net'
   MAIL_PORT = 587
   MAIL_USE_TLS = True
   MAIL_USERNAME = 'apikey'
   MAIL_PASSWORD = os.environ.get('SENDGRID_API_KEY')
   MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')


class DevConfig(BaseConfig):
   ENV_NAME = 'Development'
   DEBUG = True
   SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI')


class ProductionConfig(BaseConfig):
   ENV_NAME = 'Production'
   SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URI')


class TestConfig(BaseConfig):
   ENV_NAME = 'Development'
   TESTING = True
   DEBUG = True
   SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI')