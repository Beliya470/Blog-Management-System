# from flask import Blueprint, request, jsonify, make_response, session
# from werkzeug.security import generate_password_hash, check_password_hash
# from models import User, BlogPost, Review, db
# from flask_login import login_user, logout_user, login_required, current_user

# routes = Blueprint('routes', __name__)


# # User Routes
# @routes.route('/signup', methods=['POST'])
# def signup():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')
    
#     if not username or not password:
#         return jsonify({'message': 'Username and Password are required!'}), 400
    
#     user = User.query.filter_by(username=username).first()
#     if user:
#         return jsonify({'message': 'Username already exists!'}), 400
    
#     new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
#     db.session.add(new_user)
#     db.session.commit()
    
#     return jsonify({'message': 'User created successfully!'}), 201


# @routes.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')
    
#     user = User.query.filter_by(username=username).first()
#     if not user or not check_password_hash(user.password, password):
#         return jsonify({'message': 'Invalid Username or Password!'}), 401
    
#     login_user(user)
#     return jsonify({'message': 'Logged in successfully!'}), 200


# @routes.route('/logout', methods=['POST'])
# @login_required
# def logout():
#     logout_user()
#     return jsonify({'message': 'Logged out successfully'}), 200


# # BlogPost Routes
# @routes.route('/blogposts', methods=['GET'])
# def get_blogposts():
#     blogposts = BlogPost.query.all()
#     return jsonify([bp.as_dict() for bp in blogposts]), 200


# @routes.route('/blogposts', methods=['POST'])
# @login_required
# def create_blogpost():
#     data = request.get_json()
#     title = data.get('title')
#     content = data.get('content')
    
#     if not title or not content:
#         return jsonify({'message': 'Title and Content are required!'}), 400
    
#     new_blogpost = BlogPost(title=title, content=content, user_id=current_user.id)
#     db.session.add(new_blogpost)
#     db.session.commit()
    
#     return jsonify({'message': 'BlogPost created successfully!'}), 201


# @routes.route('/blogposts/<int:blogpost_id>', methods=['PUT', 'DELETE'])
# @login_required
# def modify_delete_blogpost(blogpost_id):
#     blogpost = BlogPost.query.get(blogpost_id)
    
#     if not blogpost:
#         return jsonify({'message': 'BlogPost not found!'}), 404
    
#     if request.method == 'PUT':
#         data = request.get_json()
#         blogpost.title = data.get('title', blogpost.title)
#         blogpost.content = data.get('content', blogpost.content)
#         db.session.commit()
#         return jsonify({'message': 'BlogPost updated successfully!'}), 200
        
#     elif request.method == 'DELETE':
#         db.session.delete(blogpost)
#         db.session.commit()
#         return jsonify({'message': 'BlogPost deleted successfully!'}), 200


# # Review Routes
# @routes.route('/reviews', methods=['POST'])
# @login_required
# def create_review():
#     data = request.get_json()
#     content = data.get('content')
#     blogpost_id = data.get('blogpost_id')
    
#     if not content or not blogpost_id:
#         return jsonify({'message': 'Content and BlogPost ID are required!'}), 400
    
#     new_review = Review(content=content, user_id=current_user.id, blogpost_id=blogpost_id)
#     db.session.add(new_review)
#     db.session.commit()
    
#     return jsonify({'message': 'Review created successfully!'}), 201


# @routes.route('/reviews/<int:review_id>', methods=['PUT', 'DELETE'])
# @login_required
# def modify_delete_review(review_id):
#     review = Review.query.get(review_id)
    
#     if not review:
#         return jsonify({'message': 'Review not found!'}), 404
    
#     if request.method == 'PUT':
#         data = request.get_json()
#         review.content = data.get('content', review.content)
#         db.session.commit()
#         return jsonify({'message': 'Review updated successfully!'}), 200
        
#     elif request.method == 'DELETE':
#         db.session.delete(review)
#         db.session.commit()
#         return jsonify({'message': 'Review deleted successfully!'}), 200
