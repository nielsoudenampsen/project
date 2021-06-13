import os
import requests
import urllib.parse

from flask import redirect,session
from functools import wraps

def eur(num):
    """Format value as EUR."""
    return f"${num:,.2f}"

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def lookup_recipe(recipe):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://tasty.p.rapidapi.com/recipes/list"

        querystring = {"prefix":recipe}

        headers = {
                    'x-rapidapi-key': "fc22b0d256mshde2ff2b2d8a7be7p17c446jsn25f2a74c339d",
                    'x-rapidapi-host': "tasty.p.rapidapi.com"
                  }
        response = requests.request("GET", url, headers=headers, params=querystring)
        
        
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    # try:
    #     quote = response.json()
    #     return {
    #         "name": quote["companyName"],
    #         "price": float(quote["latestPrice"]),
    #         "symbol": quote["symbol"]
    #     }
    # except (KeyError, TypeError, ValueError):
    #     return None

def lookup_recipes(start,size,tag,query):
    """Look up quote for symbol."""

    api_key = os.environ.get("API_KEY")

    url = "https://tasty.p.rapidapi.com/recipes/list"

    querystring = {"from":str(start),"size":str(size),"tags":tag,"q":query}

    headers = {
        'x-rapidapi-key': "70b3c859d5msh890f11222aa8ad9p14afddjsnc35eec10b6a7",
        'x-rapidapi-host': "tasty.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.json()
    return  {"description": response["results"][0]["description"],
            "name": response["results"][0]["name"]}