from flask_sqlalchemy import SQLAlchemy
import marshmallow
from flask_login import LoginManager

db = SQLAlchemy()
ma = marshmallow
login_manager = LoginManager()

def init_db(app):
    db.init_app(app)
