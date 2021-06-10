from flask import Flask,render_template,request,redirect, session

app = Flask(__name__)

@app.route('/')
def home():
    recepten = [    {"naam":"Kip Tantori","text":"Een heerlijke knor maaltijd met kip en groenten."},
                    {"naam":"Nasi goreng","text":"Een heerlijke knor maaltijd met rijst en kip."},
                    {"naam":"Bami","text":"Een heerlijke knor maaltijd met bami en varkensvlees."},
                    {"naam":"Hamburger","text":"Een zelfgemaakte hamburger met blauwe kaas."}]
    return render_template('index.html',recepten=recepten)

@app.route('/toevoegen',methods=['GET', 'POST'])
def recept_toevoegen():
    return render_template('recept_toevoegen.html')
    
@app.route('/mijn_recepten',methods=['GET', 'POST'])
def mijn_recepten():
    return render_template('mijn_recepten.html')
    
@app.route('/stats',methods=['GET', 'POST'])
def stats():
    return render_template('stats.html')
    
@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        print("post")
        return redirect("/")
    else:
        return redirect("/")
    return render_template('login.html')
    
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
        return redirect("/")
    else:
        return render_template('register.html')