"""
Auth module, contains of login, logout and social network authorization modules, now vk only
"""
from flask import request, redirect, render_template, url_for, g, session, Blueprint
from flask_login import login_user, logout_user, current_user
from app import lm
from app.models import User, ROLE_USER
from app.vk_api import VkApi
from app.secrets import vk_client_id, vk_secret_key
from urllib.request import urlopen, Request
import json


auth_module = Blueprint('auth', __name__, template_folder='templates')


@auth_module.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template('login.html')


@auth_module.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@lm.user_loader
def load_user(email):
    """
    function for flask_login package, it checks exist user or not
    :param email: the id of user
    :return: None if no user in base, user if user exists
    """
    user = User.objects(email=email)
    if not user:
        return None
    return User.objects.get(email=email)


@auth_module.route('/try_vk_auth')
def try_vk_auth():
    """
    try get code from vk.com for authorization
    :return: redirect to vk_auth page with code or error
    """
    vk_auth_page = url_for('auth.vk_auth', _external=True)
    req_url = 'https://oauth.vk.com/authorize?client_id=' + vk_client_id + \
              '&scope=email&redirect_uri=' + vk_auth_page + \
              '&response_type=code&v=5.52'
    return redirect(req_url)


@auth_module.route('/vk_auth')
def vk_auth():
    """
    Authorization using vk OAuth, getting user email, first name, last name and avatar
    :return: redirect to index page if all is ok else redirect to login page again
    """
    vk_auth_page = url_for('auth.vk_auth', _external=True)
    code = request.args.get('code', '')
    access_token_url = 'https://oauth.vk.com/access_token?client_id=' + vk_client_id + \
                       '&client_secret=' + vk_secret_key + '&code=' + code + '&redirect_uri=' + vk_auth_page
    req = Request(url=access_token_url)
    response = urlopen(req).read()
    response = json.loads(response.decode('utf-8'))
    if 'access_token' in response and 'email' in response:
        access_token = response['access_token']
        email = response['email']
        user = User.objects(email=email)
        user_id = response['user_id']
        vk_api = VkApi(token=access_token)
        req_result = vk_api.call_api('users.get', params={'user_id': user_id, 'fields': 'photo_50,screen_name'})
        nickname = email.split('@')[0]
        avatar_url = ''
        if req_result:
            if 'last_name' in req_result[0].keys() and 'first_name' in req_result[0].keys():
                nickname = req_result[0]['first_name'] + ' ' + req_result[0]['last_name']
            if 'photo_50' in req_result[0].keys():
                avatar_url = req_result[0]['photo_50']
        if not user:
            user = User(nickname=nickname, email=email, role=ROLE_USER, avatar_url=avatar_url)
        else:
            user = User.objects.get(email=email)
            user.nickname = nickname
            if avatar_url:
                user.avatar_url = avatar_url
        user.save()
        remember_me = False
        if 'remember_me' in session:
            remember_me = session['remember_me']
            session.pop('remember_me', None)
        login_user(user, remember=remember_me)
        return redirect(request.args.get('next') or url_for('main.index'))
    elif 'error' in response:
        return redirect(url_for('auth.login'))


@auth_module.before_request
def before_request():
    g.user = current_user
