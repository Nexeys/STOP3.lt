import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

from helpers import login_required, usd, comma_format
from db import get_db_connection

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.jinja_env.filters["usd"] = usd
app.jinja_env.filters["comma_format"] = comma_format

@app.context_processor
def inject_hud_data():
    """Automatically sends user stats to the HUD in layout.html on every page."""
    if "user_id" in session:
        conn = get_db_connection()

        user = conn.execute(
            "SELECT username FROM users WHERE id = ?",
            (session["user_id"],)
        ).fetchone()

        if user:
            return {"hud_username": user["username"]}
        
    return {}


@app.route("/")
@login_required
def index():
    """
    Display the user's main portfolio dashboard.
    Fetches the logged-in user's profile information from the database
    and renders the home screen.
    """
    conn = get_db_connection()
    game = conn.execute("SELECT cash, subscribers, current_month FROM games WHERE user_id = ? AND status = 'ACTIVE'", (session["user_id"],)).fetchone()
    conn.close()

    return render_template("index.html", game = game)


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
        
        conn = get_db_connection()
        
        existing_user = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
        if existing_user:
            conn.close()
            flash("That username is already registered!")
            return redirect("/register")
        
        hashed_password = generate_password_hash(password)
        
        conn.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hashed_password))
        session["user_id"] = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()["id"]
        conn.execute("INSERT INTO games (user_id) VALUES (?)", (session["user_id"],))
        conn.commit()
        conn.close()
        
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
        
        conn = get_db_connection()

        user_row = conn.execute("SELECT id, hash FROM users WHERE username = ?", (username,)).fetchone()
        if not user_row:
            conn.close()
            flash("Username doesn't exist! Please try again.")
            return redirect("login")
        
        if not check_password_hash(user_row["hash"], password):
            conn.close()
            flash("Incorrect password! Please try again.")
            return redirect("/login")
        
        flash("Succesfully logged in!")
        session["user_id"] = user_row["id"]
        conn.close()
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
    flash("Logged out successfully.")
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)