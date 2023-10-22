import os
import subprocess
from flask import Flask, redirect, url_for, send_from_directory
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_session import Session
from extensions import db, ma, login_manager, init_db
from routes import routes as blueprint_routes
from models import User
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

app = Flask(__name__, static_folder='client/build')

# Configuration from Environment Variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'mysecret')  # It's better to have the secret key in the .env file
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'postgres://mydbuser:VJHIlImxAJWNqdTEWp8b6CjhSt5R4eeQ@dpg-ckmj8trj89us73djks30-a.oregon-postgres.render.com/myprojectdb_5gp1')  
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'postgresql://mydbuser:VJHIlImxAJWNqdTEWp8b6CjhSt5R4eeQ@dpg-ckmj8trj89us73djks30-a.oregon-postgres.render.com/myprojectdb_5gp1')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True

# Initialize Extensions
init_db(app)

# Setup Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

# CORS and Session Initialization
CORS(app, origins=["http://localhost:3000"])
Session(app)

# Flask-Migrate Initialization
migrate = Migrate(app, db)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

login_manager.login_view = 'routes.login'


@app.route('/healthz')
def health_check():
    return "OK", 200


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path == "":
        return redirect(url_for('routes.home'))
    elif os.path.exists("client/build/" + path):
        return send_from_directory('client/build', path)
    else:
        return send_from_directory('client/build', 'index.html')


app.register_blueprint(blueprint_routes, url_prefix='/routes')

def run_frontend():
    frontend_path = "../client/src"  # Path relative to the server directory; adjust if necessary
    return subprocess.Popen(["npm", "start"], cwd=frontend_path)

# Create all database tables and run the frontend development server
with app.app_context():
    db.create_all()
    run_frontend()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
