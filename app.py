import requests
from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()

@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')

@app.route('/login/', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username!="" and password!="":
        cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s",
                       (str(username), str(password)))
        records = list(cursor.fetchall())
        print("records: ", records)
        if records != []:
            return render_template('account.html', full_name=records[0][1],
                               log=records[0][2], passw=records[0][3])
        else:
            return render_template('error.html',
                                   err="There's no such user in the database")
    else:
        return render_template('error.html',
                               err="It's impossible noy to enter anything")

app.run()