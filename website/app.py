import subprocess
import sqlite3
from flask import Flask
from flask import render_template, request, redirect, url_for, g

app = Flask(__name__) 

app.run()

@app.route("/")
def home():
    return render_template("home.html")
