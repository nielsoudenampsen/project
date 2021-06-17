import os, json
from pprint import pprint

from flask import Flask,flash,render_template,request,redirect, session,url_for
from flask.helpers import get_flashed_messages
from flask_session import Session
from cs50 import SQL
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash, pbkdf2_bin
from helpers import login_required,eur,lookup_recipes


app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["eur"] = eur

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///recipe.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

@app.route('/to_favorite',methods=['POST'])
@login_required
def favorite():
    
    print(favorite)
    return render_template('index.html',favorite=favorite)     


@app.route('/',methods=['GET', 'POST'])
@login_required
def home():
    
    if request.method == "POST":
        favorite = request.form.get("recipe_to_favorite")
        print(favorite)
        search = request.form.get('search')
        recipes = lookup_recipes(0,1000,"",str(search))
    else:
        recipes = None
        favorite = None
    
    return render_template('index.html',recipes=recipes,favorite=favorite)

@app.route('/toevoegen',methods=['GET', 'POST'])
@login_required
def recept_toevoegen():
    return render_template('recept_toevoegen.html')
    
@app.route('/my_recipes',methods=['GET', 'POST'])
@login_required
def my_recipes():
    return render_template('my_recipes.html')
    
@app.route('/stats',methods=['GET', 'POST'])
@login_required
def stats():
    return render_template('stats.html')

@app.route('/logout',methods=['GET','POST'])
def logout():
    session.clear()
    flash("Logged out succesful","success")
    # for msg in get_flashed_messages():
    #     print(msg)
    return render_template('login.html')


@app.route('/login',methods=['GET', 'POST'])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        # Ensure username was submitted
        if not username:
            flash("Must provide username","danger")
            return render_template('login.html')

        # Ensure password was submitted
        elif not password:
            flash("Must provide password","danger")
            return render_template('login.html')

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE name = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("Invalid username and/or password","danger")
            return render_template('login.html')

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash("Welcome, {}".format(username),"success")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if not username:
            flash("You must provide a username","danger")
            return redirect('/register')

        if not password:
            flash("You must provide a password","danger")
            return redirect('/register')

        if not confirm:
            flash("You must confirm the password","danger")
            return redirect('/register')
        
        if password != confirm:
            flash("Password does not match","danger")
            return render_template('register.html')

        rows = db.execute("SELECT * FROM users WHERE name = ?",username)
        if len(rows) != 0:
            flash("Username already exist","danger")
            return redirect('/register')

        db.execute("INSERT INTO users (name,hash) VALUES (?,?)",username,generate_password_hash(password=password,method='pbkdf2:sha256',salt_length=8))
        flash("Registerd succesfully","success")
        return redirect("/")
    else:
        return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)