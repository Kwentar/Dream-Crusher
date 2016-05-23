from flask import Blueprint, render_template, redirect, url_for, g, request
from flask_login import login_required, current_user
from app.forms import DreamsForm
from app.models import Dream
from flask_mongoengine.wtf import model_form
dream_module = Blueprint('dreams', __name__, template_folder='templates')


@dream_module.route('/dreams', methods=['GET', 'POST'])
@login_required
def dreams():
    dreams_form = DreamsForm(request.form)
    if g.user is not None:
        current_month = g.user.get_current_month()
        if request.method == 'POST' and dreams_form.validate():
            for dream in current_month.dreams:
                a = dreams_form.dreams
                b = dreams_form.dreams.data
                curr_dream = next((x for x in dreams_form.dreams.data if x['id_'] == str(dream.id_)), None)
                if curr_dream:
                    dream.title = curr_dream['title']
                    dream.estimated_time = curr_dream['estimated_time']
            current_month.save()
            return redirect(url_for('main.index'))
        if current_month:
            if len(current_month.dreams) != 3:
                current_month.dreams.clear()
                for _ in range(3):
                    dream = Dream()
                    current_month.dreams.append(dream)
                current_month.save()
            for i in range(len(current_month.dreams)):
                dreams_form.dreams[i].id_.data = str(current_month.dreams[i].id_)
                dreams_form.dreams[i].title.data = current_month.dreams[i].title
                dreams_form.dreams[i].estimated_time.data = current_month.dreams[i].estimated_time
            return render_template('dreams.html', form=dreams_form)
    return redirect(url_for('main.index'))


@dream_module.route('/dreams/edit')
@login_required
def dreams_edit():
    return """edit <a href="{{ url_for('dreams.dreams')}}">back</a>"""


@dream_module.route('/dreams/remove')
@login_required
def dreams_remove():
    return """remove <a href="{{ url_for('dreams.dreams')}}">back</a>"""


@dream_module.route('/dreams/add')
@login_required
def dreams_add():
    return """add <a href="{{url_for('dreams.dreams')}}">back</a>"""


@dream_module.before_request
def before_request():
    g.user = current_user
