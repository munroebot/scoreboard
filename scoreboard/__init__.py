from flask import Flask, request, session, jsonify, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('scoreboard.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET'])
def index():
    return jsonify({"status":200})

@app.route('/remote', methods=['GET'])
def remote():
    return render_template('remote.html')

@app.route('/twitchoverlay', methods=['GET'])
def twitchoverlay():
    conn = get_db_connection()
    sql = "select team, label, score from scores"
    scores = conn.execute(sql).fetchall()
    conn.close()
    return render_template('overlay.html',scores=scores)

@app.route('/editlabel', methods=['GET'])
def edit_label():
    pass

@app.route('/hardreset', methods=['GET'])
def hardreset():
    conn = get_db_connection()
    with open('create.sql') as f:
        conn.executescript(f.read())    
    
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

@app.route('/score/', methods=['GET'])
def get_score():
    conn = get_db_connection()
    sql = "select team, label, score from scores"
    scores = conn.execute(sql).fetchall()
    conn.close()
    us = scores[0]
    them = scores[1]

    return jsonify({"us":[us['label'],us['score']],"them":[them['label'],them['score']]})

