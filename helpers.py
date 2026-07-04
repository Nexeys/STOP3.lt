from functools import wraps
from flask import redirect, session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def usd(value):
    if value is None:
        return "$0.00"  
    else:
        return f"${value / 100:,.2f}"