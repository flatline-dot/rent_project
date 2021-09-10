import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, '..', 'webapp.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'ddfd9fe00023232m3dcdsfvnkkcvdpde'
REMEMBER_COOKIE_DURATION = timedelta(days=5)
