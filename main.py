from flask import Flask, request, render_template, flash
from flask_mail import Mail, Message
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_recaptcha import ReCaptcha
import requests
import json
import os

app = Flask(__name__, static_folder='static', static_url_path='')

app.config['FLASK_ADMIN_SWATCH'] = 'cosmo'
app.config['DEBUG'] = False
app.config['MAIL_DEBUG'] = False
app.config['SECRET_KEY'] = app.secret_key
app.config['RECAPTCHA_ENABLED'] = True
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LdyFI4UAAAAALqiPp7HSOW4lxrRXB55M-8OWOON'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdyFI4UAAAAACkoL9_JHuTE15huwB_BMvHX58aa'
app.config['MAIL_SERVER'] = 'elcorinc-net.mail.protection.outlook.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://et_admin:3gx%hR5X@elcordatabaseserver.database.windows.net:1433/ElcorWebsiteDatabase'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 5000

db = SQLAlchemy(app)


CORS(app)

mail = Mail(app)
recaptcha = ReCaptcha(app=app)
#admin = Admin(app)
login_manager = LoginManager(app)
app.secret_key = os.urandom(25)

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, username, password):
        self.username = username
        self.password = password


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


@app.route('/', methods=['GET'])
def index():
    return render_template("//index.html")


@app.route('/reasons', methods=['GET'])
def reasons():
    return render_template("reasons.html")


@app.route('/contact-us', methods=['GET'])
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        r = requests.post('https://www.google.com/recaptcha/api/siteverify',
                          data={'secret': '6LdyFI4UAAAAACkoL9_JHuTE15huwB_BMvHX58aa',
                                'response': request.form['g-recaptcha-response']})
        google_response = json.loads(r.text)

        if google_response['success']:
            contact_form = {'name': request.form['name'],
                            'email': request.form['email'],
                            'message': request.form['message']}
            msg = Message(subject='Contact from website',
                          sender=contact_form['email'],
                          recipients=['support@elcorinc.net'],
                          body=contact_form['message'])
            mail.send(msg)
            flash('Success, we will respond within at least 24 hours.')
            return render_template('contact.html')

        else:
            flash('failed to submit, please retry or contact us at support@elcorinc.net')
            return render_template('contact.html')

    return render_template('contact.html')


@app.route('/support', methods=['GET'])
@cross_origin(origins=["http://lt.elcorinc.net:8040"])
def support():
    return render_template('support.html')


@app.route('/about', methods=['GET'])
def about():

    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    #Make google validation into helper function!
    if request.method == 'POST':
        r = requests.post('https://www.google.com/recaptcha/api/siteverify',
                          data={'secret': '6LdyFI4UAAAAACkoL9_JHuTE15huwB_BMvHX58aa',
                                'response': request.form['g-recaptcha-response']})
        google_response = json.loads(r.text)

        if google_response['success']:
            login_form = {'user': request.form['User'],
                          'password': request.form['Password']}

            #if username and password exist query for the user and validate password (add hash soon)
            if login_form['user']:
                user_ob = User.query.filter_by(username=login_form['user']).first()

                if user_ob == None:
                    flash('Incorrect password or username, please try again.')
                    return render_template('internal/login.html')

                if user_ob.password == login_form['password']:
                    return render_template('internal/success.html')

                flash('Incorrect password or username, please try again.')
                return render_template('internal/login.html')

            flash('No username or password has been entered.')
            return render_template('internal/login.html')

    return render_template('internal/login.html')


if __name__ == '__main__':
    user = User('sterling', 'derp')
    db.session.add(user)
    db.session.commit()
    db.create_all()
    app.run()

