from flask import Flask, redirect, url_for
import subprocess
from flask_migrate import Migrate
from flask_cors import CORS
from flask_session import Session
from extensions import db, ma, login_manager, init_db
from routes import routes as blueprint_routes
from models import User

app = Flask(__name__)

# Flask Configuration
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True

# Initialize Extensions using init_db function
init_db(app)

CORS(app, origins=["http://localhost:3000"])
Session(app)
migrate = Migrate(app, db)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

login_manager.login_view = 'routes.login'

@app.route('/')
def index():
    return redirect(url_for('routes.home'))

app.register_blueprint(blueprint_routes, url_prefix='/routes')

def run_frontend():
    frontend_path = "../client/src"  # adjust as per your folder structure
    return subprocess.Popen(["npm", "start"], cwd=frontend_path)

# This will be triggered when the Flask app starts
with app.app_context():
    db.create_all()
    run_frontend()

if __name__ == '__main__':
    app.run(debug=True)
