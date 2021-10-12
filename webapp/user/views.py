 # -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from webapp.user.form import LoginForm, RegistrationForm
from webapp.ads.forms import UserAd
from webapp.model import db, User, Flat


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
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('ads.index'))
    form = RegistrationForm()
    return render_template('user/registration.html', form=form)


@blueprint.route('/process-regisration', methods=["POST"])
def process_registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, role='user', phone_number=form.phone_number.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегестрировались')
        return redirect(url_for('user.login'))
    flash('Пожалуйста исправьте ошибки в форме')
    return redirect(url_for('user.registration'))


@blueprint.route('/user')
@login_required
def user():
    form = UserAd()
    return render_template('user/new_ad.html', form=form)


@blueprint.route('/process_add', methods=["POST"])
def process_add():
    form = UserAd(request.form)
    if form.validate_on_submit():
        new_ad = Flat(user_id=User.query.filter(User.username == current_user.username).first().id,
                      num_rooms=form.rooms.data,
                      price=form.price.data,
                      area=form.area.data,
                      material=form.material.data,
                      metro=form.metro.data,
                      street=form.adress.data,
                      commission=form.commission.data,
                      deposit=form.deposit.data,
                      )
        db.session.add(new_ad)
        db.session.commit()
    flash('Объявление размещено!')
    return redirect(url_for('ads.index'))
