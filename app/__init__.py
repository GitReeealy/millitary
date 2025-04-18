from flask import Flask

from .config import SQLALCHEMY_DATABASE_URI, SECRET_KEY
from .database import db
from .routes import common
from .models import init_db



def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # Инициализация расширений
    db.init_app(app)

    # Регистрация маршрутов
    app.register_blueprint(common.bp)

    @app.context_processor
    def utility_processor():
        return dict(getattr=getattr)

    # Инициализация базы данных
    with app.app_context():
        init_db()

    return app
