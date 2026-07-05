from functools import wraps
from flask import redirect, session

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