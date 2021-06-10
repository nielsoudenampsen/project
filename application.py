from flask import Flask,render_template,request,redirect, session

app = Flask(__name__)

@app.route('/')
def home():
    recepten = [    {"naam":"Kip Tantori","text":"Een heerlijke knor maaltijd met kip en groenten."},
                    {"naam":"Nasi goreng","text":"Een heerlijke knor maaltijd met rijst en kip."},
                    {"naam":"Bami","text":"Een heerlijke knor maaltijd met bami en varkensvlees."},
                    {"naam":"Hamburger","text":"Een zelfgemaakte hamburger met blauwe kaas."}]
    print(recepten)
    return render_template('index.html',recepten=recepten)

@app.route('/toevoegen')
def recept_toevoegen():
    return render_template('recept_toevoegen.html')
    
@app.route('/mijn_recepten')
def mijn_recepten():
    return render_template('mijn_recepten.html')
    
@app.route('/stats')
def stats():
    return render_template('stats.html')
    
@app.route('/login')
def login():
    return render_template('login.html')
    
@app.route('/register')
def register():
    return render_template('register.html')