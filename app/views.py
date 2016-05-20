from flask import request, flash, redirect, render_template, url_for, g, session
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm
from app import app, lm, oid, db
from app.models import User, ROLE_ADMIN, ROLE_USER
# goals = Blueprint('goals', __name__, template_folder='templates')


@app.route('/')
@login_required
def index():
    user = g.user
    return render_template('index.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html', title='Sign In', form=form, providers=app.config["OPENID_PROVIDERS"])


@app.before_request
def before_request():
    g.user = current_user


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.objects(email__exists='email')
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email, role=ROLE_USER)
        user.save()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember_me=remember_me)
    return redirect(request.args.get('next') or url_for(index))
# goals.add_url_rule('/', view_func=index)
# goals.add_url_rule('/login', view_func=login, methods=['GET', 'POST'])

