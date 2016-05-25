from flask import Blueprint, render_template, g, request, jsonify
from time import gmtime, strftime
from flask_login import login_required, current_user
from app.models import Month, DreamDay, Dream
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
        month.dreams.append(Dream(title="be better than yesterday"))
        month.dreams.append(Dream(title="collect all pokemons"))
        month.dreams.append(Dream(title="learn to fly"))
        g.user.months.append(month)
        g.user.save()

    return render_template('index.html', current_n_month=current_n_month)


@main_module.route('/add_half_hour', methods=['POST'])
@login_required
def add_half_hour():
    dream_id = request.form['dream_id']
    curr_month = g.user.get_current_month()
    curr_dream = next(x for x in curr_month.dreams if str(x.id_) == dream_id)
    curr_dream.current_time += 1
    curr_dream_day = next((x for x in curr_month.dream_days if
                          x.number == datetime.datetime.today().day and x.dream_id == curr_dream.id_), None)
    if curr_dream_day:
        curr_dream_day.current_time += 1
    else:
        dream_day = DreamDay(dream_id=dream_id)
        curr_month.dream_days.append(dream_day)
    g.user.save()
    return jsonify({'id_': dream_id})


@main_module.before_request
def before_request():
    g.user = current_user
