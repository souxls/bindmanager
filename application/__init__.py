#-*-coding:utf8-*-
import os
from flask import Flask
from flask_login import LoginManager

os.environ['APP_CONFIG_FILE'] = os.path.abspath('config/app.cfg')
app = Flask(__name__, instance_relative_config=True)
app.config.from_envvar('APP_CONFIG_FILE')
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from .views.dashboard import dashboard
app.register_blueprint(dashboard)
from .views.dns import dns
app.register_blueprint(dns)
from .views.login import auth 
app.register_blueprint(auth)
from .views.profile import profile
app.register_blueprint(profile)
