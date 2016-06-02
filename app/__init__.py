from flask import Flask, render_template
from flask_login import LoginManager
from flask_mongoengine import MongoEngine
from flask_wtf import CsrfProtect

app = Flask(__name__)
app.jinja_env.line_statement_prefix = '#'
app.config.from_pyfile('config.py')
app.config['MONGODB_SETTINGS'] = {
    'db': 'dream-crusher',
    'host': 'ds038379.mlab.com',
    'port': 38379,
    'username': 'mongo-user',
    'password': 'BHDYyA2G'
}
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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)
