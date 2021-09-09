from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from webapp.user.form import LoginForm
from webapp.model import User


blueprint = Blueprint('user', __name__)


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('ads.index'))
    form = LoginForm()
    return render_template('user/login.html', form=form)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вы вошли на сайт')
            return redirect(url_for('ads.index'))
    flash('Неверное имя пользователя или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('ads.index'))
