from flask import Blueprint, request, jsonify, make_response, redirect, url_for, render_template
# from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, validators
from models import User, BlogPost, Review, db
from extensions import ma, login_manager
import jwt
from datetime import datetime, timedelta

SECRET_KEY = 'your_secret_key'  # You should store this securely, not in the code.

def generate_token_for_user(user):
    """ Generate a JWT token for the user """
    expiration = datetime.utcnow() + timedelta(hours=1)  # Token valid for 1 hour
    token = jwt.encode({
        'user_id': user.id,
        'exp': expiration
    }, SECRET_KEY, algorithm='HS256')
    return token
routes = Blueprint('routes', __name__)

class UserForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

class BlogPostForm(FlaskForm):
    title = StringField('Title', [validators.Length(min=1, max=100), validators.DataRequired()])
    content = StringField('Content', [validators.DataRequired()])

class ReviewForm(FlaskForm):
    content = StringField('Content', [validators.DataRequired()])
    blogpost_id = StringField('BlogPost ID', [validators.DataRequired()])

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class BlogPostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BlogPost

class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review

@routes.after_request
def apply_caching(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    if 'Set-Cookie' in response.headers:
        response.headers['Set-Cookie'] = response.headers['Set-Cookie'] + '; Secure'
    return response

@routes.route('/', methods=['GET'])
def home():
    return "Welcome to the Blog Management System"

# @routes.route('/', methods=['GET'])
# def home():
#     return "Welcome to Blog Management System"

@routes.route('/signup', methods=['POST'])
def signup():
    data = request.form if request.form else request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': f'Missing value. Username: {username}, Password: {password}'}), 400
    if len(username) < 4 or len(username) > 25:
        return jsonify({'message': f'Invalid username length: {len(username)} for username: {username}'}), 400
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'message': 'Username already exists!'}), 400
    new_user = User(username=username, password=generate_password_hash(password, method='scrypt'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully! Please proceed to login.'}), 201


@routes.route('/login', methods=['POST'])
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

@routes.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    user_blogposts = BlogPost.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', username=current_user.username, blogposts=user_blogposts)

@routes.route('/logout', methods=['POST', 'OPTIONS'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully!'}), 200

# BlogPost Routes
@routes.route('/blogposts', methods=['GET'])
@login_required
def get_blogposts():
    blogposts = BlogPost.query.all()
    if blogposts:
        return BlogPostSchema(many=True).jsonify(blogposts), 200
    else:
        return jsonify([]), 200

@routes.route('/blogposts', methods=['POST'])
@login_required
def create_blogpost():
    form = BlogPostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_blogpost = BlogPost(title=title, content=content, user_id=current_user.id)
        db.session.add(new_blogpost)
        db.session.commit()

        return jsonify({'message': 'BlogPost created successfully!'}), 201

    return jsonify({'message': 'Invalid Input!'}), 400

@routes.route('/blogposts/<int:blogpost_id>', methods=['PATCH'])
@login_required
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

@routes.route('/blogposts/<int:blogpost_id>', methods=['DELETE'])
@login_required
def delete_blogpost(blogpost_id):
    blogpost = BlogPost.query.get(blogpost_id)

    if not blogpost:
        return jsonify({'message': 'BlogPost not found!'}), 404
    
    db.session.delete(blogpost)
    db.session.commit()
    return jsonify({'message': 'BlogPost deleted successfully!'}), 200

# Review Routes
@routes.route('/reviews', methods=['POST'])
@login_required
def create_review():
    form = ReviewForm()
    if form.validate_on_submit():
        content = form.content.data
        blogpost_id = form.blogpost_id.data

        new_review = Review(content=content, user_id=current_user.id, blogpost_id=blogpost_id)
        db.session.add(new_review)
        db.session.commit()

        return jsonify({'message': 'Review created successfully!'}), 201

    return jsonify({'message': 'Invalid Input!'}), 400

@routes.route('/reviews/<int:review_id>', methods=['PATCH'])
@login_required
def modify_review(review_id):
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review.query.get(review_id)

        if not review:
            return jsonify({'message': 'Review not found!'}), 404
        
        review.content = form.content.data
        db.session.commit()

        return jsonify({'message': 'Review updated successfully!'}), 200

    return jsonify({'message': 'Invalid Input!'}), 400

@routes.route('/reviews/<int:review_id>', methods=['DELETE'])
@login_required
def delete_review(review_id):
    review = Review.query.get(review_id)

    if not review:
        return jsonify({'message': 'Review not found!'}), 404
    
    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Review deleted successfully!'}), 200
