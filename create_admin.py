from getpass import getpass
import sys

from webapp.model import db, User
from webapp import create_app

app = create_app()

with app.app_context():
    username = input('Введите имя пользователя: ')
    if User.query.filter(User.username == username).count():
        print('Такой пользователь уже есть!')
        sys.exit(0)

    password = getpass('Ведите пароль')
    password2 = getpass('Подтвердите пароль')
    if not password == password2:
        print('Пароли не совпадают')
        sys.exit(0)

    new_user = User(username=username, role='user')
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    print(f'User with id: {new_user.id} added')
