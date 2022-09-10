import bcrypt, sqlite3

from flask import Flask, request, session, jsonify, render_template, redirect, url_for
from functools import wraps

app = Flask(__name__)

app.secret_key = os.environ['SESSION_KEY']

def get_db_connection():
    conn = sqlite3.connect('scoreboard.db')
    conn.row_factory = sqlite3.Row
    return conn
    
def init_db():
    with open('create.sql') as f:
        conn = get_db_connection()
        conn.executescript(f.read())    
        conn.commit()
        conn.close()

def get_scores():
    conn = get_db_connection()
    sql = "select team, label, score, period from scores"
    scores = conn.execute(sql).fetchall()
    conn.close()
    return scores

def verify_pin(pin=None):
    conn = get_db_connection()
    sql = "select pin from pins"
    hashed_pins = conn.execute(sql).fetchall()
    hashed_pin = hashed_pins[0]['pin'].encode()

    if bcrypt.checkpw(pin.encode(), hashed_pin):
        return True
    else:
        return False

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('logged_in') == None:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

#
## Startup
#
init_db()

#
## Routes
#
@app.route('/', methods=['GET'])
def index():
    return jsonify({"status":200})

@app.route('/remote', methods=['GET'])
@login_required
def remote():
    return render_template('remote.html')

@app.route('/more', methods=['GET'])
@login_required
def more_actions():
    return render_template('more.html')

@app.route('/twitchoverlay', methods=['GET'])
def twitch_overlay():
    return render_template('overlay.html',scores=get_scores())

@app.route('/editteams', methods=['GET', 'POST'])
@login_required
def edit_label():
    if request.method == "GET":
        conn = get_db_connection()
        sql = "select team, label from scores"
        teams = conn.execute(sql).fetchall()
        conn.close()
        return render_template('edit.html',teams=teams)
    else:
        labelus = request.form.get('us')
        labelthem = request.form.get('them')

        sql1 = "update scores set label='%s' where team='us'" % (labelus)
        sql2 = "update scores set label='%s' where team='them'" % (labelthem)

        conn = get_db_connection()

        conn.execute(sql1)
        conn.execute(sql2)

        conn.commit()
        conn.close()
        return redirect('remote')

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == "GET":
        return render_template("login.html")
    else:
        pin = request.form.get('pin')
        if verify_pin(pin) == True:
            session['logged_in'] = True
            return redirect("/remote")
        else:
            session['logged_in'] = False
            error = 'Invalid credentials'
        
        return render_template('login.html',errors=error)

@app.route('/logout')
def logout():
   session.pop('logged_in', None)
   return redirect(url_for('login'))

#
## API Calls
#
@app.route('/hardreset', methods=['GET', 'POST'])
def hard_reset():
    init_db()
    return jsonify({"status":200})

@app.route('/setperiod', methods=['POST'])
def set_period():
    conn = get_db_connection()
    period = request.form.get('period')
    sql = "update scores set period = '%s'" % (period,)
    p = conn.execute(sql)
    conn.commit()
    conn.close()
    return jsonify({"status":200})

@app.route('/score', methods=['POST'])
def update_score():
    team = request.form.get('team')
    operation = request.form.get('operation')

    if (operation == "inc"):
        sql = 'update scores set score = (score + 1) where team = "%s"' % (team,)
    else:
        sql = 'update scores set score = (score - 1) where team = "%s"' % (team,)

    conn = get_db_connection()
    score = conn.execute(sql)
    conn.commit()
    conn.close()
    return jsonify({"status":200})

@app.route('/score', methods=['GET'])
def get_score():
    conn = get_db_connection()
    sql = "select team, label, score, period from scores"
    scores = conn.execute(sql).fetchall()
    conn.close()
    us = scores[0]
    them = scores[1]
    
    payload = {
        "us":[
            us['label'],
            us['score'],
            us['period']
        ],
        "them":[
            them['label'],
            them['score'],
            them['period']
        ]
    }
    return jsonify(payload)

