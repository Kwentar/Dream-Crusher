import os

WTF_SRF_ENABLED = True
SECRET_KEY = "KeepThisInRlyS3cr3t"
MONGODB_SETTINGS = {'DB': "DC_base"}
OPENID_PROVIDERS = [
    {'name': 'Vk', 'url': 'Vk'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
