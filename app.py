import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

from helpers import login_required, usd, comma_format, calculate_gain
import db

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.jinja_env.filters["usd"] = usd
app.jinja_env.filters["comma_format"] = comma_format


@app.context_processor
def inject_hud_data():
    """Automatically sends user stats to the HUD in layout.html on every page."""
    if "user_id" in session:
        user = db.get_user_data(session["user_id"])
        if user:
            return {"hud_username": user["username"], "penalty": db.get_game_data(session["user_id"])["base_cancel_penalty"] * 100}
    return {}


@app.route("/")
@login_required
def index():
    """
    Display the user's main portfolio dashboard.
    Fetches the logged-in user's profile information from the database
    and renders the home screen.
    """
    game = db.get_game_data(session["user_id"])
    portfolios = db.get_portfolio_data(game["id"])
    gain = db.get_last_month(game["id"], game["current_month"])

    return render_template("index.html", game = game, portfolios = portfolios, gain = gain)


@app.route("/next")
def next_month():
    calculate_gain(session["user_id"])
    return redirect("/")


@app.route("/produce", methods=["POST"])
def produce():
    """Perform the action of buying tv show."""
    genre = request.form.get("genre")
    user_id = session["user_id"]
    if not db.produce(genre, user_id):
        flash("Not enough cash!")

    return redirect("/")


@app.route("/cancel", methods=["POST"])
def cancel():
    """Perform the action of selling tv show."""
    genre = request.form.get("genre")
    user_id = session["user_id"]
    if not db.cancel(genre, user_id, db.get_game_data(session["user_id"])["base_cancel_penalty"]):
        flash("You don't have any episodes!")

    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register(): 
    """
    Handle user account registration.
    GET: Renders the signup form page.
    POST: Validates inputs, checks for duplicate usernames, hashes passwords,
            and provisions the new user account data in the database. 
    """
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        if not username or not password or not confirmation:
            flash("You must fill out all fields!")
            return redirect("/register")
        
        if password != confirmation:
            flash("Passwords do not match!")
            return redirect("/register")        
        
        if db.check_username(username):
            flash("That username is already registered!")
            return redirect("/register")
        
        db.register_user(username, generate_password_hash(password))
        session["user_id"] = db.check_username(username)["id"]
        db.generate_new_game(session["user_id"])
        
        flash("Registration succesful!")
        return redirect("/")
    
    else:
        return render_template("register.html")
    

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Authenticate users and establish active sessions.
    GET: Renders the login page.
    POST: Processes credentials, matches against database hashes,
            and assigns the user ID to the cookie session.
    """
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password")

        if not username or not password:
            flash("You must fill out all fields!")
            return redirect("/login")

        user_row = db.check_username(username)
        if not user_row:
            flash("Username doesn't exist! Please try again.")
            return redirect("/login")
        
        if not check_password_hash(user_row["hash"], password):
            flash("Incorrect password! Please try again.")
            return redirect("/login")
        
        flash("Succesfully logged in!")
        session["user_id"] = user_row["id"]
        return redirect("/")
    else:   
        return render_template("login.html")


@app.route("/logout")
def logout():
    """
    Log the user out of the application.
    Clears all temporary data from the session cookie and redirects to login.
    """
    session.clear()
    flash("Logged out succesfully.")
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)