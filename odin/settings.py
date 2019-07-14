import os

DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
DB_NAME = os.environ['DB_NAME']
DYNAMODB_HOST = os.environ['DYNAMODB_HOST']
DYNAMODB_USER_CREDENTIALS_TABLE = os.environ['DYNAMODB_USER_CREDENTIALS_TABLE']
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
