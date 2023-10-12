from flask import Flask, redirect, url_for, send_from_directory
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_session import Session
from extensions import db, ma, login_manager, init_db
from routes import routes as blueprint_routes
from models import User
import os

app = Flask(__name__, static_folder='client/public')  # Updated this line

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True

init_db(app)
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
    if path != "" and os.path.exists(app.static_folder + '/' + path):  # Updated this line
        return send_from_directory(app.static_folder, path)  # Updated this line
    else:
        return send_from_directory(app.static_folder, 'index.html')  # Updated this line

app.register_blueprint(blueprint_routes, url_prefix='/routes')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
