from crypt import methods
from flask import Flask, render_template
from flask import request
from flask import Response
import time
from flask import Flask, request, jsonify, current_app, g as app_ctx
import psycopg2
import gc
import hashlib

diable_gc = False               #możemy wyłączyć garbage collector dla zmniejszenia "szumów"
gc_after_every_request = False  #podobnie ale tym razem powodujemy że garbage collector jest bardziej przewidywalny


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
    current_app.logger.warn('%s ns %s %s %s', time_in_ms, request.method, request.path, dict(request.args))
    return response


def comapre_string(a,b):
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True

def comapre_string_safe(a,b):
    same = True
    for i in range(min(len(a),len(b))):
        if (a[i] != b[i]):
            same = False
    return same


@app.route("/auth", methods=['POST'])
def auth():
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost", port="5432")
    curr = conn.cursor()
    username = request.form['username']
    password = request.form['password']
    curr.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
    if curr.fetchone():
        return Response("Success", status=200)
    else:
        return Response("Wrong username od password", status=401)
    if comapre_string(username, "admin") and comapre_string(password, "ping2024"):
        return Response("Success", status=200)
    else:
        return Response("Fail", status=401)



