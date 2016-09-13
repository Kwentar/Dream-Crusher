from flask import Blueprint, render_template, g, request, jsonify
from time import gmtime, strftime
from flask_login import login_required, current_user
from app.models import Month, DreamDay, Dream
import datetime


pomodoro_module = Blueprint('pomodoro', __name__, template_folder='templates')


@pomodoro_module.route('/')
@login_required
def index():
    return render_template('pomodoro.html')


@pomodoro_module.before_request
def before_request():
    g.user = current_user
