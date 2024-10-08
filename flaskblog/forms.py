from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from flaskblog.models import User
from flask import flash

class RegistrationForm(FlaskForm):
    username = StringField('Имя: ',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email: ',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Пароль: ', validators=[DataRequired()])
    confirm_password = PasswordField('Подтверждение пароля: ',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

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
                        validators=[DataRequired(), Email()])
    password = PasswordField('Пароль: ', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class AddCommentForm(FlaskForm):
    body = StringField('Ваш комментарий: ', validators=[InputRequired()])
    submit = SubmitField('Опубликовать')

class UpdateAccountForm(FlaskForm):
    username = StringField('Имя: ',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email: ',
                        validators=[DataRequired(), Email()])
    picture = FileField('Обновить фото профиля: ', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
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
    title = StringField('Заголовок: ', validators=[DataRequired()])
    content = TextAreaField('Содержание: ', validators=[DataRequired()])
    picture = FileField('Добавить фотографию: ', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Выложить')

class UpdatePostForm(FlaskForm):
    title = StringField('Заголовок: ', validators=[DataRequired()])
    content = TextAreaField('Содержание: ', validators=[DataRequired()])
    picture = FileField('Обновить фотографию: ', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Выложить')


class UpdateCommentForm(FlaskForm):
    body = StringField('Заголовок: ', validators=[InputRequired()])
    submit = SubmitField('Опубликовать')

class RequestResetForm(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    submit = SubmitField('Сбросить пароль')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            flash('Нет аккаунта с такой электронной почтой!!!', 'danger')
            raise ValidationError('There is no account with that email. You must register first')
        
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Пароль: ', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль: ', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Сбросить пароль')