import os
basedir = os.path.abspath(os.path.dirname(__file__)) # contains the location of the app.db in main directory
uploads_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app/uploads')
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'agile-project'
    # configs SQLALCHEMY_DATABASE_URI from environment variable if it exists,
    # else config from database named app.db located in the main directory
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    POST_PER_PAGE = 3
    # File upload settings
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app/uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Max upload size: 16MB