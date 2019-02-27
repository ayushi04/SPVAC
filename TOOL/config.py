import os

DEBUG = True
PORT = 8082
HOST = '0.0.0.0'
BASE_DIR = os.getcwd()
UPLOADS_DIR = os.path.join(BASE_DIR, 'static/uploads/')
STATIC_DIR = os.path.join(BASE_DIR, 'static/')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
DATABASE_CONNECT_OPTIONS = {}
THREADS_PER_PAGE = 2
CSRF_ENABLED = True
CSRF_SESSION_KEY = "secret"
SECRET_KEY = "secret"
