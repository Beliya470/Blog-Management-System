from faker import Faker
from app import db, app  # Adjust the import here to import the app instance
from models import User, BlogPost, Review  # Adjust as per your models
import random

fake = Faker()

def seed_users(number_of_users):
    for _ in range(number_of_users):
        user = User(username=fake.user_name(), password='password')
        db.session.add(user)
    db.session.commit()

def seed_blog_posts(number_of_posts):
    users = User.query.all()
    for _ in range(number_of_posts):
        post = BlogPost(
            title=fake.sentence(),
            content=fake.text(),
            user_id=random.choice(users).id
        )
        db.session.add(post)
    db.session.commit()

def seed_reviews(number_of_reviews):
    posts = BlogPost.query.all()
    users = User.query.all()
    for _ in range(number_of_reviews):
        review = Review(
            content=fake.text(),
            user_id=random.choice(users).id,
            blogpost_id=random.choice(posts).id
        )
        db.session.add(review)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():  # Use app instance to push the application context
        seed_users(10)
        seed_blog_posts(30)
        seed_reviews(100)
