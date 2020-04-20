# import os
import re
from random import randrange

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, get_flashed_messages
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
# from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, check, convert

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# pattern of a typical word
w_pattern = "(?!\s)(\w+)(((?!\s)(\W)?)\w+)?"
email_pattern = "(\w+|(\w+)\.(\w+)|(\w+)-(\w+)|(\w+)_(\w+))@(\w+|(\w+)-archive)\.(com|org|cc)"

#--- Encode and Decode method ---#
def encode(inp, step, secret=None):
    if secret == None:
        return convert(inp, step) 
    else:
        return inp.replace(secret, "*" + convert(secret, step) + "*")

# to decode, the encoder must input their submitted step and encoded secret (not the submitted!)
def decode(inp, step, secret=None):
    return encode(inp, step*(-1), secret)
#-----------------------------#
    
# Configure CS50 Library to use SQLite database
# https://www.blog.pythonlibrary.org/2017/12/12/flask-101-adding-a-database/
db = SQL("sqlite:///contact.db", connect_args={'check_same_thread': False})

@app.route("/")
def index():
    # Clear working session whenever hit "refresh"
    session.clear()
    return render_template("home.html")

@app.route("/home")
def home():
    return redirect("/")

@app.route("/guidance")
def guidance():
    session.clear()
    return render_template("guidance.html")

@app.route("/product", methods=["GET", "POST"])
def product():
    # Clear working session when clicking on Home
    session.clear()
    # Get link
    if request.method == 'GET':
        return render_template("product.html")
    else:
        method = request.form.get("method")
        if not method:
            return apology("must select a coding method")

        secret = request.form.get("secret")
        if not secret:
            secret = None
        elif len(secret) > 255 or secret.isalpha() == False:
            return apology("must be a set of aphabetical letters,\nexcluding special characters")
        
        inp = request.form.get("input")
        if not inp:
            return apology("must input your words in text box")
        text = check(inp)

        # Generate output
        if method == "encode":
            step = randrange(101, 203)
            output = encode(text, step, secret)
        else:
            step = request.form.get("step")
            if not step or step.isdigit() == False or int(step) <= 0:
                return apology("to DECODE, must pick a positive integer as KEY")
            # Try to hide the key generation algorithm
            if int(step) not in range(101, 204):
                step = randrange(101, 203)
            else:
                step = int(step)         
            output = decode(text, step, secret)
        
        # d_secret = enconded_secret
        if secret == None:
            d_secret = "No input"
        else:
            d_secret = convert(secret, step)
        # Return the final result
        return render_template("result.html", method=method, step=step, secret=secret, d_secret = d_secret, inp=text, output=output)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    ''' Leave info if visitors would like to contact us'''
    # Clear working session when clicking on Home
    session.clear()
    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == 'GET':
        # Contact info: Email, Phone number/Zalo/Viber, Skype
        return render_template("contact.html")
    else:
        # Get info from form request
        name = request.form.get("name")
        others = request.form.get("others")
        
        email = request.form.get("email")
        if not email or not re.search(email_pattern, email):
            return apology("invalid email address")

        phone = request.form.get("phone")
        if not phone:
            pass 
        elif phone.isdigit == False or len(phone) != 10:
            return apology("invalid phone number")
        
        content = request.form.get("content")
        if not content:
            return apology("must input your feedback/comment")

        # Insert info into table "info"
        db.execute("INSERT INTO info(email, name, phone, others, content) VALUES(:email, :name, :phone, :others, :content)",
                    email=email, name=name, phone=phone, others=others, content=content
                    )
        # Return home after submit
        flash("Contact info submitted!")            
        return render_template("home.html")
    
    
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)