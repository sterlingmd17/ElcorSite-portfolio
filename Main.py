from flask import Flask, request, redirect, render_template, session, flash
from App import app

@app.route('/', methods=['POST', 'GET'])
def index():

    return render_template("index.html")


if __name__ == '__main__':
    app.run()