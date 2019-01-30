from flask import Flask, request, redirect, render_template, session, flash
from App import app

@app.route('/', methods=['GET'])
def index():

    return render_template("index.html")


@app.route('/reasons', methods=['GET'])
def reasons():

    return render_template("reasons.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name=request.form()


    return render_template("contact.html")




if __name__ == '__main__':
    app.run()