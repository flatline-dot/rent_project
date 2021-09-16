from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectMultipleField, widgets, BooleanField, RadioField
from wtforms.validators import DataRequired, InputRequired


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class FilterForm(FlaskForm):
    price_min = IntegerField('price_min', render_kw={'class': 'form-control'})
    price_max = IntegerField('price_max', render_kw={'class': 'form-control'})
    rooms = [(0, 'Студия'), (1, '1'), (2, '2'), (3, '3'), (4, '4')]
    rooms = MultiCheckboxField('rooms', choices=rooms, coerce=int, render_kw={'class': "form-check-input"})
    area_min = IntegerField('area_min', render_kw={'class': 'form-control'})
    area_max = IntegerField('area_max', render_kw={'class': 'form-control'})
    type_material = [("Кирпичный", 'Кирпичный'), ("Монолитный", 'Монолитный'), ("Панельный", 'Панельный')]
    material = MultiCheckboxField('material', choices=type_material, coerce=str)
    commission = BooleanField('Без коммиссии')
    deposit = BooleanField('Без залога')


class UserAd(FlaskForm):
    rooms = [(0, 'Студия'), (1, '1'), (2, '2'), (3, '3'), (4, '4')]
    rooms = RadioField('Количество комнат', choices=rooms, coerce=int, render_kw={'class': "form-check-input"}, validators=[InputRequired()])
    price = IntegerField('Цена', render_kw={'class': 'form-control'}, validators=[DataRequired()])
    area = IntegerField('Площадь', render_kw={'class': 'form-control'})
    type_material = [("Кирпичный", 'Кирпичный'), ("Монолитный", 'Монолитный'), ("Панельный", 'Панельный')]
    material = RadioField('material', choices=type_material, validators=[DataRequired()])
    commission = IntegerField('Комиссия', render_kw={'class': 'form-control'}, validators=[DataRequired()])
    deposit = IntegerField('Залог', render_kw={'class': 'form-control'}, validators=[DataRequired()])
    metro = StringField('Метро', render_kw={'class': 'form-control'}, validators=[DataRequired()])
    phone = IntegerField('Номер телефона', render_kw={'class': 'form-control'}, validators=[DataRequired()])
    adress = StringField('Адрес', render_kw={'class': 'form-control'}, validators=[DataRequired()])
