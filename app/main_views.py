from flask import Blueprint, render_template, g
from time import gmtime, strftime
from flask_login import login_required, current_user
from app.models import Month, User
import datetime


main_module = Blueprint('main', __name__, template_folder='templates')


@main_module.route('/')
@login_required
def index():
    current_month = strftime("%B", gmtime())
    n_month = int(strftime("%m", gmtime()))
    year = datetime.datetime.today().year
    exist = False
    for m in g.user.months:
        if m.n_month == n_month and m.year == year:
            exist = True
            break;
    if not exist:
        month = Month(name=current_month, n_month=n_month, year=year)
        month.save()
        g.user.months.append(month)
        g.user.save()

    return render_template('index.html', month=current_month)


@main_module.before_request
def before_request():
    g.user = current_user
