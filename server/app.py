# Apply patch first
# from patch import apply_patch
# apply_patch()

from flask import Flask, redirect, url_for, send_from_directory
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_session import Session
from extensions import db, ma, login_manager, init_db
from routes import routes as blueprint_routes
from models import User
import os
import subprocess

app = Flask(__name__, static_folder='client/build')

# Increase the Maximum Request Header Size
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Set to 16 MB or adjust as needed

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

# Flask Configuration
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True

# Initialize Extensions using init_db function
init_db(app)

# Other Initializations
CORS(app, origins=["http://localhost:3000"])
Session(app)
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
    frontend_path = "../client/src"  # adjust as per your folder structure
    return subprocess.Popen(["npm", "start"], cwd=frontend_path)

# This will be triggered when the Flask app starts
with app.app_context():
    db.create_all()
    run_frontend()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
