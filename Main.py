from flask import Flask,request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_recaptcha import ReCaptcha
import requests
import json

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']='mysql://elcor:elcor@localhost:3306/elcor'
app.config['SQLALCHEMY_ECHO'] = True
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LdsiZIUAAAAAJybnDIelA5soDfns61EHnTrN2Ha'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdsiZIUAAAAAN4LVoj1xQxyMmFyV_AA6NFwGh0B'
app.secret_key= "elcor"
recaptcha = ReCaptcha(app=app)
db = SQLAlchemy(app)


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/reasons', methods=['GET'])
def reasons():
    return render_template("reasons.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact():

    if request.method == 'POST':
        form_name = request.form['name']
        form_email = request.form['email']
        form_message = request.form['message']
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data={'secret': app.config['RECAPTCHA_PRIVATE_KEY'],
                                                                                  'response': request.form['g-recaptcha-response']})
        google_response = json.loads(r.text)
        print(google_response)
        print(request.form)
        if google_response['success']:
            flash('success')
            return render_template('contact.html')
        else:
            flash('failed captcha')
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