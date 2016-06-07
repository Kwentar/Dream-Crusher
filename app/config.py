import os
from app.secrets import secret_key, mongo_db_settings
WTF_CSRF_ENABLED = True
SECRET_KEY = secret_key
MONGODB_SETTINGS = mongo_db_settings

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
