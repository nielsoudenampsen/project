import os
import requests
import urllib.parse
from pprint import pprint
from cs50 import SQL

from flask import redirect,session
from functools import wraps

db = SQL("sqlite:///recipe.db")

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

def lookup_recipes(start,size,tag,query):
    """Look up quote for symbol."""
    try:

        api_key = os.environ.get("API_KEY")

        url = "https://tasty.p.rapidapi.com/recipes/list"

        querystring = {"from":str(start),"size":str(size),"tags":tag,"q":query}

        headers = {
            'x-rapidapi-key': "cbc9c244d1mshbc7142f4dcf7d59p15a492jsn04e851823481",
            'x-rapidapi-host': "tasty.p.rapidapi.com"
            }

        response = requests.request("GET", url, headers=headers, params=querystring).json()
        print(db.execute('SELECT * FROM recipes'))
        db.execute('INSERT INTO recipes (search,json) VALUES ?,?',query,response)

        recipes = []
        for i in range(len(response["results"])):
            recipes.append({
                "description": response["results"][i]["description"],
                "name": response["results"][i]["name"],
                "img": response["results"][i]["thumbnail_url"]
                })

    except requests.RequestException:
        return None

    return recipes
    