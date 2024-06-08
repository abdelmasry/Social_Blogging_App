from app import db
from app.models import User, Post
from sqlalchemy.exc import IntegrityError
import random
from faker import Faker

fake = Faker()


def users(count=100):
    for i in range(count):
        u = User(
            email=fake.email(),
            username=fake.user_name(),
            password="password",
            name=fake.name(),
            location=fake.city(),
            about_me=fake.text(),
            member_since=fake.past_date(),
        )
        db.session.add(u)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def posts(count=100):
    user_count = User.query.count()
    for i in range(count):
        u = User.query.offset(random.randint(0, user_count - 1)).first()
        p = Post(body=fake.text(), timestamp=fake.past_date(), author=u)
        db.session.add(p)
    db.session.commit()
