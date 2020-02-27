# Third party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Local app imports
from config import Config

# Globally accessible libraries
db = SQLAlchemy()
# compare_type=True so flask-migrate tracks column type changes
migrate = Migrate(compare_type=True)


def create_app(config_class=Config):
    """Application factory returns Flask application object"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import web_bp
    app.register_blueprint(web_bp)

    from .routes import api_bp
    app.register_blueprint(api_bp)

    return app


from partyparser import models  # noqa: F401
