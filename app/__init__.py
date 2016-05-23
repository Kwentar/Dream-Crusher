from flask import Flask
from flask_login import LoginManager
from flask_mongoengine import MongoEngine
from flask_wtf import CsrfProtect

app = Flask(__name__)

app.config.from_pyfile('config.py')
CsrfProtect(app)
db = MongoEngine(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'auth.login'

from app.auth_views import auth_module
from app.main_views import main_module
from app.dreams_views import dream_module

app.register_blueprint(auth_module)
app.register_blueprint(dream_module)
app.register_blueprint(main_module)


if __name__ == "__main__":
    app.run(debug=True)
