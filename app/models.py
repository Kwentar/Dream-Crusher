import datetime
from app import db
from flask_login import UserMixin
from flask import url_for
from mongoengine import *


class Goal(db.Document):
    created_time = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    estimated_time = db.IntField(min_value=1, required=False)
    current_time = db.IntField(required=True, default=0)

    def __unicode__(self):
        return self.title

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_time'],
        'ordering': ['title']
    }

ROLE_ADMIN = 0
ROLE_USER = 1


class User(db.Document, UserMixin):
    nickname = db.StringField(max_length=255, required=True)
    email = db.StringField(max_length=255, required=True, unique=True, primary_key=True)
    role = db.IntField(required=True, default=ROLE_USER)
    goals = db.ListField(db.EmbeddedDocumentField('Goal'))
    avatar_url = db.StringField(required=True, defaul="")

    def __unicode__(self):
        return "{} {} {}, goals: {}".format(
            self.nickname,
            self.email,
            "user" if self.role else "admin",
            ",".join([x.title for x in self.goals]))

    def get_id(self):
        return str(self.email)

    meta = {
        'indexes': ['nickname', 'email'],
        'ordering': ['nickname']
    }
