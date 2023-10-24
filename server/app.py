import os
from flask import Flask, redirect, url_for, send_from_directory, safe_join, jsonify, make_response, request, render_template
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager
from flask_session import Session
from dotenv import load_dotenv, find_dotenv
from extensions import db, ma, login_manager, init_db
from models import User, BlogPost, Review, db as app_db
import jwt
from flask_wtf import FlaskForm
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, validators
import sqlalchemy.exc

# Load Environment Variables
load_dotenv(dotenv_path=find_dotenv())

app = Flask(__name__, static_folder='client/build')

# Configuration from Environment Variables
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mysecret')


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True

# Initialize Extensions
init_db(app)

# Setup Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# CORS and Session Initialization
# CORS(app, origins=["http://localhost:3000"])
cors = CORS(app, resources={r"/*": {"origins": "*"}})
Session(app)

SECRET_KEY = 'your_secret_key'  # Store this securely, not in the code.

def generate_token_for_user(user):
    expiration = datetime.utcnow() + timedelta(hours=1)
    token = jwt.encode({
        'user_id': user.id,
        'exp': expiration
    }, app.config['SECRET_KEY'], algorithm='HS256')  # Use the secret key from app.config
    return token


DEFAULT_USER_ID = 0
# Flask-Migrate Initialization
migrate = Migrate(app, db)

# FlaskForm classes
class UserForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

class BlogPostForm(FlaskForm):
    title = StringField('Title', [validators.Length(min=1, max=100), validators.DataRequired()])
    content = StringField('Content', [validators.DataRequired()])

class ReviewForm(FlaskForm):
    content = StringField('Content', [validators.DataRequired()])
    blogpost_id = StringField('BlogPost ID', [validators.DataRequired()])

# Marshmallow Schemas (adjusted)
class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username")

class BlogPostSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "content", "user_id")

class ReviewSchema(ma.Schema):
    class Meta:
        fields = ("id", "content", "user_id", "blogpost_id")

# Define routes for your application

@app.route('/healthz')
def health_check():
    return "OK", 200

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists("client/build/" + path):
        return send_from_directory('client/build', path)
    else:
        # Here you can render a 'login.html' or similar if you want
        # return render_template('login.html')
        return "Welcome to the Blog Management System!", 200  # Simple message for now

@app.route('/signup', methods=['POST'])
def signup():
    data = request.form if request.form else request.get_json()

    # data = request.form if request.form else request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': f'Missing value. Username: {username}, Password: {password}'}), 400
    if len(username) < 4 or len(username) > 25:
        return jsonify({'message': f'Invalid username length: {len(username)} for username: {username}'}), 400
    try:
        user = User.query.filter_by(username=username).first()
    except sqlalchemy.exc.OperationalError as e:
        return "Database connection error: " + str(e), 500

    if user:
        return jsonify({'message': 'Username already exists!'}), 400
    new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully! Please proceed to login.'}), 201

@app.route('/login', methods=['OPTIONS'])
def login_options():
    response = make_response()
    response.headers['Access-Control-Allow-Origin'] = '*'  # Or specify the origin you want to allow
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'POST,OPTIONS'
    return response

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'status': 'error', 'message': 'Invalid Username or Password!'}), 401

    # Assuming you have a function to generate tokens.
    token = generate_token_for_user(user)

    return jsonify({'status': 'success', 'message': 'Logged in successfully!', 'token': token}), 200

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    user_blogposts = BlogPost.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', username=current_user.username, blogposts=user_blogposts)

@app.route('/logout', methods=['POST', 'OPTIONS'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully!'}), 200

@app.route('/logout', methods=['OPTIONS'])
def logout_options():
    response = make_response()
    response.headers['Access-Control-Allow-Origin'] = '*'  # Adjust this as per your requirements
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'POST,OPTIONS'
    return response

# BlogPost Routes
@app.route('/blogposts', methods=['GET'])
def get_blogposts():
    blogposts = BlogPost.query.all()
    blogposts_data = []

    for post in blogposts:
        post_data = post.to_dict()  # assuming `to_dict()` exists for the BlogPost model
        post_data['reviews'] = [review.to_dict() for review in post.reviews]
        blogposts_data.append(post_data)

    return jsonify(blogposts_data), 200

@app.route('/blogposts', methods=['POST'])
# @login_required
def create_blogpost():
    data = request.form
    print("Received data:", data)
    title = data.get('title')
    content = data.get('content')
    image = request.files.get('image')  # Getting the uploaded file. You can process it further if needed.

    if not title or not content:
        return jsonify({'message': 'Title and content are required!'}), 400

    default_user_id = 1  # or fetch the id of a default user from your database

    if current_user.is_authenticated:
        user_id = current_user.id
    else:
        user_id = default_user_id

    new_blogpost = BlogPost(title=title, content=content, user_id=user_id)

    db.session.add(new_blogpost)
    db.session.commit()

    blogpost_data = BlogPostSchema().dump(new_blogpost)

    return jsonify({'message': 'BlogPost created successfully!', 'blogPost': blogpost_data, 'success': True}), 201

@app.route('/blogposts/<int:blogpost_id>', methods=['GET'])
def get_single_blogpost(blogpost_id):
    blogpost = BlogPost.query.get(blogpost_id)
    if blogpost:
        return BlogPostSchema().jsonify(blogpost), 200
    else:
        return jsonify({"message": "BlogPost not found!"}), 404

@app.route('/blogposts/<int:blogpost_id>', methods=['PATCH'])
# @login_required
def modify_blogpost(blogpost_id):
    form = BlogPostForm()
    if form.validate_on_submit():
        blogpost = BlogPost.query.get(blogpost_id)

        if not blogpost:
            return jsonify({'message': 'BlogPost not found!'}), 404

        blogpost.title = form.title.data
        blogpost.content = form.content.data
        db.session.commit()

        return jsonify({'message': 'BlogPost updated successfully!'}), 200

    return jsonify({'message': 'Invalid Input!'}), 400

@app.route('/blogposts/<int:blogpost_id>', methods=['DELETE'])
# @login_required
def delete_blogpost(blogpost_id):
    blogpost = BlogPost.query.get(blogpost_id)

    if not blogpost:
        return jsonify({'message': 'BlogPost not found!'}), 404

    db.session.delete(blogpost)
    db.session.commit()
    return jsonify({'message': 'BlogPost deleted successfully!'}), 200

# Review Routes

@app.route('/reviews/<int:review_id>', methods=['PATCH'])
# @login_required
def modify_review(review_id):
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review.query.get(review_id)

        if not review:
            return jsonify({'message': 'Review not found!'}), 404

        review.content = form.content.data
        user_exists = User.query.get(review.user_id)
        if user_exists:
            db.session.commit()
        else:
            print(f"User with user_id {review.user_id} doesn't exist!")

        db.session.rollback()

        # db.session.commit()

        return jsonify({'message': 'Review updated successfully!'}), 200

    return jsonify({'message': 'Invalid Input!'}), 400

@app.route('/reviews/<int:review_id>', methods=['DELETE'])
# @login_required
def delete_review(review_id):
    review = Review.query.get(review_id)

    if not review:
        return jsonify({'message': 'Review not found!'}), 404

    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Review deleted successfully!'}), 200

# Get all reviews for a specific blogpost
@app.route('/blogposts/<int:blogpost_id>/reviews', methods=['GET'])
def get_reviews_for_blogpost(blogpost_id):
    blogpost = BlogPost.query.get(blogpost_id)
    if not blogpost:
        return jsonify({"message": "BlogPost not found!"}), 404

    reviews = blogpost.reviews  # Assuming you have a relationship defined in BlogPost for reviews
    reviews_data = [ReviewSchema().dump(review) for review in reviews]
    return jsonify(reviews_data), 200

# Create a review for a specific blogpost
@app.route('/blogposts/<int:blogpost_id>/reviews', methods=['POST'])
def add_review_to_blogpost(blogpost_id):
    blogpost = BlogPost.query.get(blogpost_id)
    if not blogpost:
        return jsonify({"message": "BlogPost not found!"}), 404

    data = request.json
    review_text = data.get('content')

    # review_text = data.get('text')
    if not review_text:
        return jsonify({"message": "Review text is required!"}), 400

    # Use current user's ID or fallback to the default user ID
    user_id = getattr(current_user, 'id', DEFAULT_USER_ID)

    new_review = Review(content=review_text, user_id=int(user_id), blogpost_id=int(blogpost_id))
    # new_review = Review(content=review_text, user_id=user_id, blogpost_id=blogpost_id)
    db.session.add(new_review)
    db.session.commit()

    return jsonify({"message": "Review added successfully!", "review": ReviewSchema().dump(new_review)}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 'db' should refer to the same database instance used throughout your app.
        # run_frontend()  # Uncomment this if it's necessary and correctly defined.
        app.run()  # This starts your Flask application.
