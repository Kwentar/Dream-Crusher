from functools import wraps
from flask import Blueprint, g, render_template, request
from flask_login import login_required, current_user
from app.models import ROLE_ADMIN

admin_module = Blueprint('admin', __name__, template_folder='templates')


def required_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if g.user.role not in roles:
                return "You dont have permission to view this page."
            return f(*args, **kwargs)
        return wrapped
    return wrapper


'''
    sms api doc: http://sms.ru/?panel=api&subpanel=method&show=sms/send
'''


@admin_module.route('/admin', methods=['POST', 'GET'])
@login_required
@required_roles(ROLE_ADMIN)
def admin():
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        return render_template('admin.html')


@admin_module.before_request
def before_request():
    g.user = current_user
