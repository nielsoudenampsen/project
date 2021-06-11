from flask import Flask,render_template,request,redirect, session
from flask_session import Session
from cs50 import SQL
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash, pbkdf2_bin
from helpers import login_required,eur


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

@app.route('/')
@login_required
def home():
    
    recepten = [    {"naam":"Kip Tantori","text":"Een heerlijke knor maaltijd met kip en groenten."},
                    {"naam":"Nasi goreng","text":"Een heerlijke knor maaltijd met rijst en kip."},
                    {"naam":"Bami","text":"Een heerlijke knor maaltijd met bami en varkensvlees."},
                    {"naam":"Hamburger","text":"Een zelfgemaakte hamburger met blauwe kaas."}]

    return render_template('index.html',recepten=recepten)

@app.route('/toevoegen',methods=['GET', 'POST'])
@login_required
def recept_toevoegen():
    return render_template('recept_toevoegen.html')
    
@app.route('/mijn_recepten',methods=['GET', 'POST'])
@login_required
def mijn_recepten():
    return render_template('mijn_recepten.html')
    
@app.route('/stats',methods=['GET', 'POST'])
@login_required
def stats():
    return render_template('stats.html')
    
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
            msg = "must provide username"
            return render_template('register.html',msg=msg)

        # Ensure password was submitted
        elif not password:
            msg = "must provide password"
            return render_template('register.html',msg=msg)

        # Query database for username
        rows = db.execute("SELECT * FROM gebruikers WHERE naam = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            msg = "invalid username and/or password"
            return render_template('register.html',msg=msg)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
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
            msg = "You must provide a username"
            return render_template('register.html',msg=msg)

        if not password:
            msg = "You must provide a password"
            return render_template('register.html',msg=msg)

        if not confirm:
            msg = "You must confirm the password"
            return render_template('register.html',msg=msg)
        
        if password != confirm:
            msg = "Password does not match"
            return render_template('register.html',msg=msg)

        rows = db.execute("SELECT * FROM gebruikers WHERE naam = ?",username)
        print(len(rows))
        if len(rows) != 0:
            msg = "Username already exist"
            return render_template('register.html',msg=msg)

        db.execute("INSERT INTO gebruikers (naam,password) VALUES (?,?)",username,generate_password_hash(password=password,method='pbkdf2:sha256',salt_length=8))
        return redirect("/")
    else:
        return render_template('register.html')