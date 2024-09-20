from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Имя: ',
                           validators=[DataRequired(), Length(min=4, max=20, message="Имя должно быть от 4 до 20 символов")])
    email = StringField('Email: ',
                        validators=[DataRequired(), Email("Некорректный email")])
    password = PasswordField('Пароль :', validators=[DataRequired(), Length(min=4, max=20, message="Пароль должен быть от 4 до 20 символов")])
    confirm_password = PasswordField('Повтор пароля: ',
                                     validators=[DataRequired(), EqualTo('password', message="Пароли не совпадают")])
    submit = SubmitField('Регистрация')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя уже занято. Пожалуйста, введите другое')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Этот email уже занят. Пожалуйста, введите другой')


class LoginForm(FlaskForm):
    email = StringField('Email: ',
                        validators=[DataRequired(), Email("Некорректный email")])
    password = PasswordField('Пароль: ', validators=[DataRequired(), Length(min=4, max=100, message="Пароль должен быть от 4 до 100 символов")])
    remember = BooleanField('Запомнить', default=False)
    submit = SubmitField('Войти')

class AddCommentForm(FlaskForm):
    body = StringField('Ваш комментарий', validators=[InputRequired()])
    submit = SubmitField('Опубликовать')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Обновить фото профиля', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Обновить')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Это имя уже занято. Пожалуйста, введите другое')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Этот email уже занят. Пожалуйста, введите другой')


class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(min=2, max=15)])
    content = TextAreaField('Содержание', validators=[DataRequired()])
    postpicture = FileField('Добавить фотографию', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Выложить')

class UpdatePostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(min=2, max=15)])
    content = TextAreaField('Содержание', validators=[DataRequired()])
    postpicture = FileField('Обновить фотографию', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Выложить')


class UpdateCommentForm(FlaskForm):
    body = StringField('Заголовок', validators=[InputRequired()])
    submit = SubmitField('Опубликовать')