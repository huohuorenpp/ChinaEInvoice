# -*- coding: utf-8 -*-

from flask import Flask  # 引入 flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import logging
from config import LOG_FILENAME

loginmanager = LoginManager()
loginmanager.session_protection = 'strong'
loginmanager.login_view = 'login'


app = Flask(__name__)  # 实例化一个flask 对象
handler = logging.FileHandler(LOG_FILENAME, encoding='UTF-8')
logging_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)
app.config.from_object('config')
loginmanager.init_app(app)
db = SQLAlchemy(app)

bootstrap = Bootstrap(app)# 初始化 db 对象
from app import views
from app import models