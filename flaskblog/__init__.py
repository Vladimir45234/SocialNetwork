from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flaskblog.settings import app
from flask_mail import Mail
from flask import Flask


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = "Пожалуйста, авторизируйтесь для доступа к закрытым страницам"
mail = Mail(app)

from flaskblog import routes