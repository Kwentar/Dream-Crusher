from flask_wtf import Form
from wtforms import StringField, IntegerField, FieldList, FormField, HiddenField
from wtforms import validators


class DreamForm(Form):
    id_ = HiddenField("id")
    title = StringField('Name of dream', [validators.required(), validators.length(max=80)],
                        default="New Dream, New Hope")
    estimated_time = IntegerField('Estimated time', [validators.required(), validators.number_range(min=1, max=1000)],
                                  default=40)


class DreamsForm(Form):
    dreams = FieldList(FormField(DreamForm), min_entries=3)


class SendSMSForm(Form):
    sms_text = StringField('Text of sms', [validators.required(), validators.length(max=70)])

