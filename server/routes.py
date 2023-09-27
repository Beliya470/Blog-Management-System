from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, validators
from models import User, BlogPost, Review
from extensions import ma  # Importing ma from extensions.py

routes = Blueprint('routes', __name__)

# Setup Flask-WTF Forms
class UserForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

class BlogPostForm(FlaskForm):
    title = StringField('Title', [validators.Length(min=1, max=100), validators.DataRequired()])
    content = StringField('Content', [validators.DataRequired()])

class ReviewForm(FlaskForm):
    content = StringField('Content', [validators.DataRequired()])
    blogpost_id = StringField('BlogPost ID', [validators.DataRequired()])


# Setup Marshmallow Schemas
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


class BlogPostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BlogPost


class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review


# User Routes
@routes.route('/signup', methods=['POST'])
def signup():
    from app import ma  
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.query.filter_by(username=username).first()
        if user:
            return jsonify({'message': 'Username already exists!'}), 400

        new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully!'}), 201
    
    return jsonify({'message': 'Invalid Input!'}), 400


@routes.route('/login', methods=['POST'])
def login():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({'message': 'Invalid Username or Password!'}), 401
        
        login_user(user)
        return jsonify({'message': 'Logged in successfully!'}), 200
    
    return jsonify({'message': 'Invalid Input!'}), 400


@routes.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200


# BlogPost Routes
@routes.route('/blogposts', methods=['GET'])
def get_blogposts():
    blogposts = BlogPost.query.all()
    return BlogPostSchema(many=True).jsonify(blogposts), 200


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



# # Register Blueprint
# app.register_blueprint(routes)

# if __name__ == "__main__":
#     app.run(debug=True)
