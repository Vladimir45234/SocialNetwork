from flask import Flask
import os
from flask_mail import Mail, Message
app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(36)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'v95543043@gmail.com'
app.config['MAIL_PASSWORD'] = 'xpbt iqxd iwia ftsr'

mail = Mail(app)



