from flask import request, flash, redirect, render_template, url_for, g, session
from flask_login import login_user, logout_user, current_user, login_required
from time import gmtime, strftime
from app import app, lm, db
from app.models import User, ROLE_ADMIN, ROLE_USER
from app.vk_api import VkApi
from app.secrets import vk_client_id, vk_secret_key
from urllib.request import urlopen, http, Request
import json
# goals = Blueprint('goals', __name__, template_folder='templates')


@app.route('/')
@login_required
def index():
    current_month = strftime("%B", gmtime())
    return render_template('index.html', month=current_month)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    vk_auth_page = 'http://127.0.0.1:5000/vk_auth'
    req_url = 'https://oauth.vk.com/authorize?client_id=' + vk_client_id + \
              '&scope=email&redirect_uri=' + vk_auth_page + \
              '&response_type=code&v=5.52'
    return render_template('login.html', title='Sign In', url_vk=req_url)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@lm.user_loader
def load_user(email):
    user = User.objects(email__exists='email')
    if not user:
        return None
    return User.objects.get(email=email)


@app.route('/vk_auth')
def vk_auth():
    vk_auth_page = 'http://127.0.0.1:5000/vk_auth'
    code = request.args.get('code', '')
    access_token_url = 'https://oauth.vk.com/access_token?client_id=' + vk_client_id + \
                       '&client_secret=' + vk_secret_key + '&code=' + code + '&redirect_uri=' + vk_auth_page
    req = Request(url=access_token_url)
    response = urlopen(req).read()
    response = json.loads(response.decode('utf-8'))
    if 'access_token' in response and 'email' in response:
        access_token = response['access_token']
        email = response['email']
        user = User.objects(email__exists='email')
        user_id = response['user_id']
        vk_api = VkApi(token=access_token)
        req_result = vk_api.call_api('users.get', params={'user_id': user_id,
                                                                    'fields': 'photo_50,screen_name'})
        if not user:
            nickname = email.split('@')[0]
            avatar_url = ''
            if req_result:
                if 'last_name' in req_result[0].keys() and 'first_name' in req_result[0].keys():
                    nickname = req_result[0]['first_name'] + ' ' + req_result[0]['last_name']
                if 'photo_50' in req_result[0].keys():
                    avatar_url = req_result[0]['photo_50']
            user = User(nickname=nickname, email=email, role=ROLE_USER, avatar_url=avatar_url)
            user.save()
        else:
            user = User.objects.get(email=email)
            if req_result:
                if 'last_name' in req_result[0].keys() and 'first_name' in req_result[0].keys():
                    user.nickname = req_result[0]['first_name'] + ' ' + req_result[0]['last_name']
                if 'photo_50' in req_result[0].keys():
                    user.avatar_url = req_result[0]['photo_50']
                user.save()
        remember_me = False
        if 'remember_me' in session:
            remember_me = session['remember_me']
            session.pop('remember_me', None)
        login_user(user, remember=remember_me)
        return redirect(request.args.get('next') or url_for('index'))
    elif 'error' in response:
        return redirect(url_for('login'))


@app.before_request
def before_request():
    g.user = current_user


# @oid.after_login
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

