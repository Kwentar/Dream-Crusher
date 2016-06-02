import os

WTF_CSRF_ENABLED = True
SECRET_KEY = "KeepThisInRlyS3cr3t"
MONGODB_SETTINGS = {'DB': "dream-crusher"}
MONGO_URI = 'mongodb://mongo-user:BHDYyA2G@ds038379.mlab.com:38379/dream-crusher'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
