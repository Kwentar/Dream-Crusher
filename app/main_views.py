from flask import Blueprint, render_template, g, request, jsonify
from time import gmtime, strftime
from flask_login import login_required, current_user
from app.models import Month, User
import datetime


main_module = Blueprint('main', __name__, template_folder='templates')


@main_module.route('/')
@login_required
def index():
    current_month = strftime("%B", gmtime())
    current_n_month = datetime.datetime.today().month
    current_year = datetime.datetime.today().year
    exist = False
    for m in g.user.months:
        if m.n_month == current_n_month and m.year == current_year:
            exist = True
            break
    if not exist:
        month = Month(title=current_month, n_month=current_n_month, year=current_year)
        g.user.months.append(month)
        g.user.save()

    return render_template('index.html', current_n_month=current_n_month)


@main_module.route('/add_half_hour', methods=['POST'])
@login_required
def add_half_hour():
    dream_id = request.form['dream_id']
    curr_dream = next(x for x in g.user.get_current_month().dreams if str(x.id_) == dream_id)
    curr_dream.current_time += 1
    g.user.save()
    return jsonify({'id_': dream_id})


@main_module.before_request
def before_request():
    g.user = current_user
