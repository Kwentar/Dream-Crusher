from flask import Blueprint, render_template, g
from time import gmtime, strftime
from flask_login import login_required, current_user

main_module = Blueprint('main', __name__, template_folder='templates')


@main_module.route('/')
@login_required
def index():
    current_month = strftime("%B", gmtime())
    return render_template('index.html', month=current_month)


@main_module.before_request
def before_request():
    g.user = current_user
