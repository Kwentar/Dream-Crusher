import os
from flask import Flask
from flask_login import LoginManager
from app.forms import LoginForm
from flask_mongoengine import MongoEngine

app = Flask(__name__)

app.config.from_pyfile('config.py')

db = MongoEngine(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'



# oid = OpenID(app, os.path.join(app.config["BASE_DIR"], 'tmp'))

from app.views import index, login

if __name__ == "__main__":
    app.run(debug=True)
