from flask_login import UserMixin
from extensions import db 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    blogposts = db.relationship('BlogPost', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reviews = db.relationship('Review', backref='blogpost', lazy=True)  # Changed backref to 'blogpost' to match the class name
    
    def __repr__(self):
        return f'<BlogPost {self.title}>'
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content
        }


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    blogpost_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'), nullable=False)  # Fixed the ForeignKey reference to 'blog_post.id' to match the table name
    
    def __repr__(self):
        return f'<Review {self.id}>'
    
    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "user_id": self.user_id,
            "blogpost_id": self.blogpost_id
        }
