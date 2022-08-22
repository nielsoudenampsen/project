import os, json

from flask import Flask,flash,render_template,request,redirect, session,url_for
from flask.helpers import get_flashed_messages
from flask_session import Session
from cs50 import SQL
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required,eur,lookup_recipes,isInList,take


app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["eur"] = eur
app.jinja_env.filters["isInList"] = isInList
app.jinja_env.filters["take"] = take

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_NAME"]
Session(app)

db = SQL("sqlite:///recipe.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

@app.route('/recipe/<id>',methods=['GET', 'POST'])
@login_required
def recipe_detail(id):
    name = request.form.get("name")
    img = request.form.get("img")
    description = request.form.get("description")
    return render_template("recipe_detail.html",name=name,img=img,description=description,id=id)


@app.route('/',methods=['GET', 'POST'])
@login_required
def home():
    favorites = json.loads(db.execute("SELECT favorites FROM users WHERE id = ?",session["user_id"])[0]["favorites"])
    search = request.args.get('search')
    recipes = lookup_recipes(0,1000,"",str(search))
    #top3_favorites = list(favorites.items())[0][1].get('img')
    return render_template('index.html',recipes=recipes,favorites=favorites,search=search,)#top3_favorites=top3_favorites)

@app.route('/favorite/<id>',methods=['GET','POST'])
@login_required
def favorite(id):
    if request.method == "POST":
        favorite_id = request.json['favorite_id']
        favorite_name = request.json['favorite_name']
        favorite_img = request.json['favorite_img']
        favorite_description = request.json['favorite_description']


        if id in session["favorites"]:
            session["favorites"].pop(id)
        else:
            session["favorites"][id] = {
                "description": favorite_description,
                "name": favorite_name,
                "img": favorite_img,
                "id": favorite_id
                }
       
        db.execute("UPDATE users SET favorites = ? WHERE id = ?",json.dumps(session["favorites"]),session["user_id"])
        return redirect(request.referrer)

    

@app.route('/my_recipes',methods=['GET', 'POST'])
@login_required
def my_recipes():
    favorites = json.loads(db.execute("SELECT favorites FROM users WHERE id = ?",session["user_id"])[0]["favorites"])
    return render_template('my_recipes.html',favorites=favorites)
    


@app.route('/logout',methods=['GET','POST'])
def logout():
    session.clear()
    flash("Logged out succesful","success")
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
        try:
            session["favorites"] = json.loads(db.execute("SELECT favorites FROM users WHERE id = ?",session["user_id"])[0]["favorites"])
        except:
            session["favorites"] = {}
            db.execute("UPDATE users SET favorites = ? WHERE id = ?",json.dumps(session["favorites"]),session["user_id"])
            


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

@app.route('/change-credentials',methods=['GET', 'POST'])
@login_required
def change_credentials():
    if request.method == "POST":
        password = request.form.get('password')
        confirm =  request.form.get('confirm')
        old_password_hash = db.execute("SELECT hash FROM users WHERE id = ?",session["user_id"])[0]["hash"]

        if password != confirm:
            flash("Password are not confirmed","danger")
            return redirect("/change-credentials")
        elif check_password_hash(old_password_hash,password):
            flash("Password is the same as the old password","danger")
            return redirect("/change-credentials")
        else:
            db.execute("UPDATE users SET hash = ? WHERE id = ?",generate_password_hash(password=password,method='pbkdf2:sha256',salt_length=8),session["user_id"])
            flash("Changed credentials succesful","success")
            return redirect('/')
    else:
        return render_template('change-credentials.html')

if __name__ == '__main__':
    app.run(debug=True)