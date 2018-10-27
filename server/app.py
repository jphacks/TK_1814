from database import init_db, session
from flask import Flask
from flask_basicauth import BasicAuth
from flask_migrate import Migrate
from model import db
from config import secret_key
from views import test, record, promise, motion
from admin import init_admin
# from flask_pushjack import FlaskAPNS


def init_app():
    app_obj = Flask(__name__, static_folder='uploads')
    app_obj.config.from_object('config.BaseConfig')
    app_obj.secret_key = secret_key

    init_db(app_obj)
    init_admin(app_obj)
    add_bp(app_obj)

    return app_obj


def add_bp(app_obj):
    modules_define = [
        test.app, record.app, promise.app, motion.app
    ]

    for bp_app in modules_define:
        app_obj.register_blueprint(bp_app)


app = init_app()
# client = FlaskAPNS()
# client.init_app(app)
admin_basic_auth = BasicAuth(app)
migrate = Migrate(app, db)


@app.route('/')
@app.route('/index')
def index():
    return 'This is index page'


@app.teardown_appcontext
def session_clear(exception):
    if exception and session.is_active:
        session.rollback()
    else:
        session.commit()

    session.close()
