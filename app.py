from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from webscraper import getWords
import csv
import json

# Start application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/answer", methods=(["GET", "POST"]))
def answer():
    if request.method == "POST":
        niveau = request.form["niveau"]
        set = request.form["set"]
        how = request.form["how"]
        getWords(set, how, niveau)
        with open(f"csvFiles/chap{niveau}.csv", 'r') as f:
            csv_reader = csv.DictReader(f)
            answers = list(csv_reader)
        return render_template("answer.html", answers=answers)
