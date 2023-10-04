from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_session import Session
from extensions import db, ma, login_manager
from routes import routes
from models import User  # Add this import

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True

db.init_app(app)
ma.init_app(app)
CORS(app, origins=["http://localhost:3000"])
Session(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

login_manager.init_app(app)
login_manager.login_view = 'routes.login'

app.register_blueprint(routes)  # Register the blueprint only once

Migrate(app, db)  # Initialize Migrate after all other initializations

if __name__ == '__main__':
    app.run(debug=True)
