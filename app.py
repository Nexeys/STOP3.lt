import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

from helpers import login_required, usd
from db import get_db_connection

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register(): 
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
        conn.commit()
        conn.close()
        
        flash("Registration succesful! Please log in.")
        return redirect("/login")
    
    else:
        return render_template("register.html")
    

@app.route("/login")
def login():
    return "<h3>Login page coming next! Move to the next step to build this template.</h3>"


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)