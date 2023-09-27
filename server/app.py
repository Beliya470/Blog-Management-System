from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_session import Session  # Importing Session for cookie-based session management
from extensions import db, ma, login_manager  # Importing db, ma, and login_manager from extensions.py
from routes import routes

app = Flask(__name__)  # app instance
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'  # You can also use 'redis', 'memcached' or others
app.config['SESSION_PERMANENT'] = True  # If you want the cookie to be persistent across browser restarts

db.init_app(app)
ma.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
CORS(app)
Session(app)  # Initializing the Session
Migrate(app, db)

app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)
