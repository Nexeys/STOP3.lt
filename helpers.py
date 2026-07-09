from functools import wraps
from flask import redirect, session
import db

def login_required(f):
    """
    Decorate routes to require an authenticated user session.

    Checks the active session cookie for a 'user_id'. If the user is not 
    logged in, they are redirected to the login page. If they are logged in, 
    the request proceeds to the intended route normally.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def usd(value):
    """
    Format a numeric value as US Dollar currency.

    Takes a numeric amount (representing cents) and converts it into a 
    standard, human-readable currency string with commas and two decimal places.
    Returns '$0.00' if the input value is missing or None.
    """
    if value is None:
        return "$0.00"  
    else:
        return f"${value / 100:,.2f}"
    

def comma_format(value):
    """
    Format a generic numeric value.

    Takes a numeric amount (representing cents) and converts it into a 
    standard, human-readable string
    """
    return f"{value:,}"


def calculate_gain(user_id):
    new_subscribers = 0
    event = db.get_random_event()
    game_data = db.get_game_data(user_id)
    for portfolio in db.get_portfolio_data(game_data["id"]):
        genre_subscribers = portfolio["episodes_produced"] * portfolio["base_subscriber_yield"]
        if event["specific_genre"] in (None, portfolio["genre"]):
            genre_subscribers = genre_subscribers * event["modifier_pct"] // 100
        new_subscribers += genre_subscribers

    cash = (new_subscribers + game_data["subscribers"]) * game_data["base_cash_per_subscriber"]
    db.log_month(game_data["id"], event["title"], new_subscribers, cash, game_data["current_month"])
    