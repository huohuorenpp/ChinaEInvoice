# -*- coding: utf-8 -*-


import os

basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
CSRF_ENABLED = True
LOG_FILENAME = os.path.join(basedir, 'log', 'Ei_access_logs.log')
SECRET_KEY = 'renpp-will-always-know'