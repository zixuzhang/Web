# -*- coding: utf-8 -*-
import gridfs
from flask import Flask
from flask_bootstrap import Bootstrap
from pymongo import MongoClient
from config import config
from flask_mongoengine import MongoEngine
from flask_login import LoginManager


# app = Flask(__name__)
bootstrap = Bootstrap()
db = MongoEngine()

login_manage = LoginManager()
login_manage.session_protection = 'strong'
login_manage.login_view = 'auth.login'


# client = MongoClient('localhost',27017)
# # zxjd_db = client.test
# zxjd_db = client.zxjd_database
# fs = gridfs.GridFS(zxjd_db)
# categories = zxjd_db.categories
# share_collection = zxjd_db.share
# # user = zxjd_db.user

def create_app(config_name):
    app = Flask(__name__)
    a = config[config_name]
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manage.init_app(app)


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_buleprint
    app.register_blueprint(auth_buleprint, url_prefix='/auth')

    return app





