from datetime import datetime
from flaskblog import db, login_manager, app
from flask_login import UserMixin
from hashlib import md5

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    last_seen = db.Column(db.DateTime)
    user_status = db.Column(db.String(40), nullable=True, default="Лучший пользователь проекта")

    liked = db.relationship(
        'PostLike',
        foreign_keys='PostLike.user_id',
        backref='user', lazy='dynamic')
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(
            PostLike.user_id == self.id,
            PostLike.post_id == post.id).count() > 0


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class PostLike(db.Model):
    __tablename__ = 'post_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_post = db.Column(db.String(30), nullable=False, default='default.jpg')
    
    views = db.Column(db.Integer, default=0)
    likes = db.relationship('PostLike', backref='post', lazy='dynamic')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='comment_post', lazy=True, cascade='all, delete-orphan')

    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f'Post({self.id} ,{self.title}, {self.date_posted.strftime("%d.%m.%Y-%H.%M")}, {self.image_post}, {self.user_id})'
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    body = db.Column(db.Text(200), nullable=False)
    date_comment = db.Column(db.DateTime, nullable=False, default=datetime.now)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f'Comment({self.body}, {self.date_comment.strftime("%d.%m.%Y-%H.%M")}, {self.post_id})'
