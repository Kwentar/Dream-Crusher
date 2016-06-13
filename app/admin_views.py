from functools import wraps
from urllib.request import Request, urlopen, quote

from flask import Blueprint, g, render_template, request, flash
from flask_login import login_required, current_user
from app.models import ROLE_ADMIN
from app.forms import SendSMSForm
from app import app

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
    send_sms_form = SendSMSForm(request.form)
    if request.method == 'POST' and send_sms_form.validate():
        text = send_sms_form.sms_text.data
        result = send_sms_to_me(text)
        if result:
            code = int(result.split()[0])
            if code == 100:
                flash('sms has been send successfully with text: ' + text)
            elif code in send_sms_errors.keys():
                flash('Error: ' + send_sms_errors[code])
            else:
                flash('I cant send sms, something wrong, I don\'t know what exactly :(')
        else:
            flash('I cant send sms, something wrong, I don\'t know what exactly :(')
    return render_template('admin.html', form=send_sms_form)


@admin_module.before_request
def before_request():
    g.user = current_user


def send_sms_to_me(text):
    text = quote(text.encode('cp1251'), safe="/;%[]=:$&()+,!?*@'~")
    url_ = 'http://sms.ru/sms/send?api_id=' + app.config['SMS_API_ID'] + '&to=79880116219&text=' + text
    req = Request(url=url_)
    response = urlopen(req).read()
    return response


send_sms_errors = {
    200: 'Неправильный api_id',
    201: 'не хватает средств на лицевом счету',
    202: 'Неправильно указан получатель',
    203: 'Нет текста сообщения',
    204: 'Имя отправителя не согласовано с администрацией',
    205: 'Сообщение слишком длинное (превышает 8 СМС)',
    206: 'Будет превышен или уже превышен дневной лимит на отправку сообщений',
    207: 'На этот номер (или один из номеров) нельзя отправлять сообщения, '
         'либо указано более 100 номеров в списке получателей',
    208: 'Параметр time указан неправильно',
    209: 'Вы добавили этот номер (или один из номеров) в стоп-лист',
    210: 'Используется GET, где необходимо использовать POST',
    211: 'Метод не найден',
    212: 'Текст сообщения необходимо передать в кодировке UTF-8 (вы передали в другой кодировке)',
    220: 'Сервис временно недоступен, попробуйте чуть позже.',
    230: 'Сообщение не принято к отправке, так как на один номер в день нельзя отправлять более 60 сообщений.',
    300: 'Неправильный token (возможно истек срок действия, либо ваш IP изменился)',
    301: 'Неправильный пароль, либо пользователь не найден',
    302: 'Пользователь авторизован, но аккаунт не подтвержден (пользователь не ввел код, '
         'присланный в регистрационной смс)'
}
