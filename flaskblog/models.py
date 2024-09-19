from datetime import datetime
from flaskblog import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def load_all_users():
    return User.query.all()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    last_seen = db.Column(db.DateTime)
    user_status = db.Column(db.String(40), nullable=True, default="Лучший пользователь проекта")

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    post_image = db.Column(db.String(30), nullable=False, default='default.jpg')
    
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='comment_post', lazy=True, cascade='all, delete-orphan')

    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f'Post({self.id} ,{self.title}, {self.date_posted.strftime("%d.%m.%Y-%H.%M")}, {self.post_image}, {self.user_id})'
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    body = db.Column(db.Text(200), nullable=False)
    date_comment = db.Column(db.DateTime, nullable=False, default=datetime.now)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f'Comment({self.body}, {self.date_comment.strftime("%d.%m.%Y-%H.%M")}, {self.post_id})'
