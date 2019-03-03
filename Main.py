from flask import Flask, request, redirect, render_template, session, flash
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_recaptcha import ReCaptcha
from werkzeug.security import check_password_hash
import requests
import json

app = Flask(__name__)
app.config['DEBUG'] = False
app.config['MAIL_DEBUG'] = False

app.config['RECAPTCHA_ENABLED'] = True
#app.config['SQLALCHEMY_DATABASE_URI']='mysql://elcor:elcor@localhost:3306/elcor'
#app.config['SQLALCHEMY_ECHO'] = True

app.config['RECAPTCHA_PUBLIC_KEY'] = '6LdyFI4UAAAAALqiPp7HSOW4lxrRXB55M-8OWOON'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdyFI4UAAAAACkoL9_JHuTE15huwB_BMvHX58aa'

app.config['MAIL_SERVER'] = 'elcorinc-net.mail.protection.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)
app.secret_key= "elcor"
recaptcha = ReCaptcha(app=app)
#db = SQLAlchemy(app)
#print(mail.connect())


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/reasons', methods=['GET'])
def reasons():
    return render_template("reasons.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data={'secret': app.config['RECAPTCHA_PRIVATE_KEY'],'response': request.form['g-recaptcha-response']})
        google_response = json.loads(r.text)
        print(str(google_response))

        if google_response['success'] == True:
            contact_form = { 'name' : request.form['name'], 'email' : request.form['email'], 'message' : request.form['message']}
            #form_email = request.form['email']
            #form_message = request.form['message']
            msg = Message(subject='Contact from website', sender= contact_form['email'], recipients= ['support@elcorinc.net'], body=contact_form['message'])
            #mail.send(msg)
            flash('success')
            return render_template('contact.html')

        else:
            flash('failed captcha, please retry.' + str(google_response))
            return render_template('contact.html')

    return render_template('contact.html')



# For better contact page.
#@app.route('/contact2', methods=['GET', 'POST'])
#def contact2():
#   if request.method == 'POST':
#       form_name = request.form['name']
#        form_email = request.form['email']
#        form_phone = request.form['phone']
#        form_call = request.form['call time']
#        form_comments = request.form['comments']
#
#    return render_template("contact.html")


if __name__ == '__main__':
    app.run()