from flask import Flask, request, session, jsonify, render_template, redirect
import bcrypt, sqlite3

app = Flask(__name__)

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

def check_password():
    return True

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
def remote():
    return render_template('remote.html')

@app.route('/more', methods=['GET'])
def moreactions():
    return render_template('more.html')

@app.route('/twitchoverlay', methods=['GET'])
def twitchoverlay():
    return render_template('overlay.html',scores=get_scores())

@app.route('/editteams', methods=['GET', 'POST'])
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
        if check_password(pin) == True:
            session['logged_in'] = True
            return redirect("/remote")
        else:
            session['logged_in'] = False
            error = 'Invalid credentials'
        
        return render_template('login.html',errors=error)

#
## API Calls
#
@app.route('/hardreset', methods=['GET', 'POST'])
def hardreset():
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

@app.route('/scoreboard/update', methods=['POST'])
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

    return jsonify({"us":[us['label'],us['score'],us['period']],"them":[them['label'],them['score'],them['period']]})

