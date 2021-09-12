from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from webapp.user.form import LoginForm, RegistrationForm
from webapp.model import db, User


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
            login_user(user, remember=form.remember_me.data)
            flash('Вы вошли на сайт')
            print(current_user)
            return redirect(url_for('ads.index'))
    flash('Неверное имя пользователя или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('ads.index'))


@blueprint.route('/registration')
def registation():
    if current_user.is_authenticated:
        return redirect(url_for('ads.index'))
    form = RegistrationForm()
    return render_template('user/registration.html', form=form)


@blueprint.route('/process-regisration', methods=["POST"])
def process_registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, role='user')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегестрировались')
        return redirect(url_for('user.login'))
    flash('Пожалуйста исправьте ошибки в форме')
    return redirect(url_for('user.registration'))