from operator import methodcaller
from flask import session
from flask import request, render_template, Flask, redirect, url_for, make_response
from os import urandom
import pymongo
from pymongo.errors import ConnectionFailure
import os

#account_sid = os.environ['AC8ef87725499512171f849e7a4beb8dc0']
#auth_token = os.environ['75d438aa82bc1908bba7471cbc8f9f5d']

client = pymongo.MongoClient("mongodb+srv://columbia:columbia@cluster0.ttjp4ta.mongodb.net/?retryWrites=true&w=majority")
db = client.test
try:
    client.admin.command('ping')
except ConnectionFailure:
    print("Server not available")

app = Flask(__name__)
debug = True
app.secret_key = urandom(24)

def get_file_names():
    mydb = client["user_files"]
    collection = mydb["files"]
    item_details = collection.find()
    ret = []
    for item in item_details:
        if (item["username"] == request.cookies.get('username')):
            ret.append(item["file"])
    return ret



@app.route('/register',methods = ['POST'])
def register():
    dblist = client.list_database_names()
    mydb = client["user_info"]
    mycol = mydb["customers"]
    mydict = { "username": request.form['email'], "password": request.form['password'] }
    x = mycol.insert_one(mydict)
    make_response().set_cookie('username', request.form['email'])
    return render_template("mainpage.html", login_message="Welcome, " + request.form['email'])

@app.route('/register',methods = ['GET'])
def see_register():
   return render_template("signup.html")

@app.route('/login',methods = ['POST'])
def login():
    mydb = client["user_info"]
    collection = mydb["customers"]
    item_details = collection.find()
    print('dasljk')
    for item in item_details:
        if (item["username"] == request.form['email'] and
            item["password"] == request.form['password']):
            resp = make_response(render_template("mainpage.html", login_message="Welcome, " + request.form['email']))
            print('hello')
            resp.set_cookie('username', request.form['email'])
            session["username"] = request.form['email']
            return resp
    return render_template("login.html")

@app.route('/login',methods = ['GET'])
def see_login():
    print("alksjdlkasjd")
    return render_template("login.html")



def main():
    """
    false if this file imported as module
    debugging enabled
    """
    app.config['UPLOAD_FOLDER'] = "/temp"
    app.debug = True
    app.run()


if __name__ == "__main__":
    main()