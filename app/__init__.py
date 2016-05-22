from flask import Flask
from flask_login import LoginManager
from app.forms import LoginForm
from flask_mongoengine import MongoEngine

app = Flask(__name__)

app.config.from_pyfile('config.py')

db = MongoEngine(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'auth.login'

from app.auth_views import auth_module
from app.main_views import main_module

app.register_blueprint(auth_module)
app.register_blueprint(main_module)

if __name__ == "__main__":
    app.run(debug=True)
