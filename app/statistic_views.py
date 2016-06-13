from flask import Blueprint, g, render_template, request, flash
from flask_login import login_required, current_user

statistic_module = Blueprint('statistic', __name__, template_folder='templates')


@statistic_module.route('/statistic', methods=['GET'])
@login_required
def statistic():
    return render_template('statistic.html')


@statistic_module.before_request
def before_request():
    g.user = current_user
