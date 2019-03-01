from flask import Flask
from Main import app
from flask_sqlalchemy import SQLAlchemy
from flask_recaptcha import ReCaptcha


app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']='mysql://elcor:elcor@localhost:3306/elcor'
app.config['SQLALCHEMY_ECHO'] = True
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LdsiZIUAAAAAJybnDIelA5soDfns61EHnTrN2Ha'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdsiZIUAAAAAN4LVoj1xQxyMmFyV_AA6NFwGh0B'
app.secret_key= "elcor"
recaptcha = ReCaptcha(app=app)
db = SQLAlchemy(app)


