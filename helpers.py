import json
import os
import requests
import urllib.parse
from pprint import pprint
from cs50 import SQL

from flask import redirect,session
from functools import wraps

from sqlalchemy.sql.expression import false

db = SQL("sqlite:///recipe.db")

def isInList(search,list):
    """Checks if item is in the dict"""
    for item in list:
        if str(search) == str(item):
            return True
    else:
        return False

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
        if query == None:
            return None
        if query == "":
            return None
        if query == "None":
            return None
        api_key = os.environ.get("API_KEY")

        url = "https://tasty.p.rapidapi.com/recipes/list"

        querystring = {"from":str(start),"size":str(size),"tags":tag,"q":query}

        headers = {
            'x-rapidapi-key': {api_key},
            'x-rapidapi-host': "tasty.p.rapidapi.com"
            }
        exist = db.execute('SELECT search FROM recipes WHERE search = ?',query)
        
        if len(exist) != 1:
            response = requests.request("GET", url, headers=headers, params=querystring)
            cache = json.dumps(response.json())
            db.execute('INSERT INTO recipes (search,json) VALUES (?,?)',query,cache)
            response = response.json()
        else:
            response = db.execute('SELECT json FROM recipes WHERE search = ?',query)
            response = response[0]['json']
            response = json.loads(response)

        recipes = []
        for i in range(len(response["results"])):
            recipes.append({
                "description": response["results"][i]["description"],
                "name": response["results"][i]["name"],
                "img": response["results"][i]["thumbnail_url"],
                "id": response["results"][i]["id"]
                })

    except requests.RequestException:
        return None

    return recipes
    