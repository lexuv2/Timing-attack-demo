from crypt import methods
from flask import Flask, render_template
from flask import request
from flask import Response
import time
from flask import Flask, request, jsonify, current_app, g as app_ctx
import psycopg2
import gc
import hashlib
from sympy import use
import sys


import config

diable_gc = False               #możemy wyłączyć garbage collector dla zmniejszenia "szumów"
gc_after_every_request = False  #podobnie ale tym razem powodujemy że garbage collector jest bardziej przewidywalny
rebuild_db = True               
if rebuild_db:
    import prepare_database
    import get_users_in_db

if diable_gc:
    gc.disable()



app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("login.html")


@app.before_request
def logging_before():
    # Store the start time for the request
    app_ctx.start_time = time.perf_counter_ns()


@app.after_request
def logging_after(response):
    if gc_after_every_request:
        gc.collect()
    # Get total time in milliseconds
    total_time = time.perf_counter_ns() - app_ctx.start_time
    time_in_ms = total_time
    # Log the time taken for the endpoint 
    #current_app.logger.warn('%s ns %s %s %s', time_in_ms, request.method, request.path, dict(request.args))
    return response


def comapre_string(a,b):
    if len(a) != len(b):
        return False
    #time.sleep(0.001)
    for i in range(len(a)):
        #time.sleep(0.001)
        if a[i] != b[i]:
            return False
    return True

def comapre_string_safe(a,b):
    same = True
    for i in range(min(len(a),len(b))):
        if (a[i] != b[i]):
            same = False
    return same

conn = psycopg2.connect(dbname=config.dbname, user=config.db_user, password=config.db_password, host=config.db_host, port=config.db_port)

@app.route("/auth", methods=['POST'])
def auth():
    
    username = request.form['username']
    password = request.form['password']
    #curr.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
    curr = conn.cursor()
    curr.execute(f"SELECT * FROM users WHERE username = '{username}'")

    user = curr.fetchone()
    curr.close()
    if user is None:
        #time.sleep(0.005)
        return "Wrong username or password",400

    password_db = user[2]
    
    if comapre_string(password_db,password):
        return "Logged in",200
    else:
        return "Wrong username or password",401
    
