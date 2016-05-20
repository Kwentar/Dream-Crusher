from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms import validators


class LoginForm(Form):
    openid = StringField('openid', [validators.required(), validators.length(max=80)])
    remember_me = BooleanField('remember_me', default=False)
