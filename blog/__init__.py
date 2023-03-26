#blog/_init_.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from blog.config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from blog.routes import bp
    app.register_blueprint(bp)

    from blog.fake_data import generate_entries

    return app







