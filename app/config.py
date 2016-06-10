import os
from app.secrets import secret_key, mongo_db_settings, sms_api_id

WTF_CSRF_ENABLED = True
SECRET_KEY = secret_key
MONGODB_SETTINGS = mongo_db_settings
SMS_API_ID = sms_api_id
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
