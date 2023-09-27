from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from extensions import db, ma, login_manager  # Importing db, ma, and login_manager from extensions.py
from routes import routes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
CORS(app)
Migrate(app, db)

app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)
