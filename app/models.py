import datetime
from app import db
from flask import url_for
from mongoengine import *


class Goal(db.Document):
    created_time = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    estimated_time = db.IntField(min_value=1, required=False)

    def __unicode__(self):
        return self.title

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_time'],
        'ordering': ['title']
    }
