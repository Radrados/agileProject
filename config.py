import os
basedir = os.path.abspath(os.path.dirname(__file__)) # contains the location of the app.db in main directory

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'agile-project'
    # configs SQLALCHEMY_DATABASE_URI from environment variable if it exists,
    # else config from database named app.db located in the main directory
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')