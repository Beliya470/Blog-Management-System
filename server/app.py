# from flask import Flask
# from flask_migrate import Migrate
# from flask_cors import CORS
# from flask_session import Session
# from extensions import db, ma, login_manager
# from flask import redirect, url_for


# # Importing routes from routes.py
# from routes import routes as blueprint_routes

# # Models
# from models import User

# # Flask Configuration
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'mysecret'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SESSION_PERMANENT'] = True

# # Initialize Extensions
# db.init_app(app)
# ma.init_app(app)
# CORS(app, origins=["http://localhost:3000"])
# Session(app)
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# login_manager.login_view = 'routes.login'

# # Registering the blueprint from routes.py
# @app.route('/')
# def index():
#     return redirect(url_for('routes.home'))
# app.register_blueprint(blueprint_routes, url_prefix='/routes')
# # app.register_blueprint(blueprint_routes)

# Migrate(app, db)  # Initialize Migrate after all other initializations

# if __name__ == '__main__':
#     app.run(debug=True)





from flask import Flask, redirect, url_for
from flask_migrate import Migrate
from flask_cors import CORS
from flask_session import Session
from extensions import db, ma, login_manager
import os
import subprocess

# Importing routes from routes.py
from routes import routes as blueprint_routes

# Models
from models import User

# Flask Configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True

# Initialize Extensions
db.init_app(app)
ma.init_app(app)
CORS(app, origins=["http://localhost:3000"])
Session(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

login_manager.login_view = 'routes.login'

# Registering the blueprint from routes.py
@app.route('/')
def index():
    return redirect(url_for('routes.home'))

app.register_blueprint(blueprint_routes, url_prefix='/routes')

Migrate(app, db)  # Initialize Migrate after all other initializations


def run_frontend():
    frontend_path = "../client/src"  # adjust as per your folder structure
    return subprocess.Popen(["npm", "start"], cwd=frontend_path)


# This will be triggered when the Flask app starts
with app.app_context():
    run_frontend()


if __name__ == '__main__':
    app.run(debug=True)
