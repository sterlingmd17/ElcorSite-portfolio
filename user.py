from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from main import app



db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://et_admin:3gx%hR5X@localhost:3306/database'
app.config['SQLALCHEMY_ECHO'] = True
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, username, password):
        self.username = username
        self.password = password


