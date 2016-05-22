from flask import Blueprint, render_template, redirect, url_for, g
from flask_login import login_required, current_user

dream_module = Blueprint('dreams', __name__, template_folder='templates')


@dream_module.route('/dreams')
@login_required
def dreams():
    if g.user is not None:
        current_month = g.user.get_current_month()
        if current_month:
            dreams_list = current_month.dreams
            return render_template('dreams.html', dreams_list=dreams_list)
    return redirect(url_for('main.index'))


@dream_module.route('/dreams/edit')
@login_required
def dreams_edit():
    return """edit <a href="{{ url_for('dreams.dreams')}}">back</a>"""


@dream_module.route('/dreams/remove')
@login_required
def dreams_remove():
    return """remove <a href="{{ url_for('dreams.dreams')}}">back</a>"""


@dream_module.route('/dreams/add')
@login_required
def dreams_add():
    return """add <a href="{{url_for('dreams.dreams')}}">back</a>"""


@dream_module.before_request
def before_request():
    g.user = current_user
