# The purpose of this file is to construct an application package to call factory functions
from flask import Flask
from flask_admin import Admin
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_caching import Cache
from config import config
from flask_pagedown import PageDown
from flask_debugtoolbar import DebugToolbarExtension
from flask_static_digest import FlaskStaticDigest

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()
csrf = CSRFProtect()
cache = Cache()

debug_toolbar = DebugToolbarExtension()
flask_static_digest = FlaskStaticDigest()
admin = Admin(template_mode='bootstrap4')

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    csrf.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    debug_toolbar.init_app(app)
    flask_static_digest.init_app(app)
    admin.init_app(app)


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .organization import organization as organization_blueprint
    app.register_blueprint(organization_blueprint, url_prefix='/organization')

    from .second_transaction import transaction as transaction_blueprint
    app.register_blueprint(transaction_blueprint, url_prefix='/transaction')

    return app
