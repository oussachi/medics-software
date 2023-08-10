from flask import Flask, redirect, url_for, render_template, request, session
from flask_session import Session
import uuid, time
from appcode.MongoDB.MongoHandler import *
from appcode.Cryptography.CryptographyHandler import *
from appcode.Messaging.EmailHandler import *
from appcode.Messaging.SMSHandler import *

DATABASE_NAME = 'medics'
CONNECTION_STRING = 'mongodb+srv://medicssoftware:sFuj1OxAiWxQt3vu@cluster0.yjfetxk.mongodb.net/?retryWrites=true&w=majority'
USER_COLLECTION = 'users'
HOST_EMAIL = 'medicssoftware@gmail.com'
HOST_EMAILPASSWORD = ''

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def home():
    return render_template('user/profile.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        userName = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        fullName = request.form["fullname"]
        bio = request.form["bio"]
        if request.files['file'].filename != '':
            filePath = request.files['file'].filename
            fileId = uploadFile(CONNECTION_STRING, DATABASE_NAME, filePath)
        else:
            fileId = None

        query = { "UserName": userName }
        user = { "UserName": userName, "Password": password, "Email": email, "FullName": fullName, "Bio": bio, "file": fileId }
        insertedId = insertDocument(CONNECTION_STRING, DATABASE_NAME, USER_COLLECTION, user)
        if (insertedId != None):
            message = 'User created successfully!!'
        else:
            message = 'Error has been occurred, Please try again!!'
    else:
        return render_template('login.html')

@app.route('/signin', methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        userName = request.form["username"]
        password = request.form["password"]

        user = { "UserName": userName, "Password": password }
        insertedId = selectDocuments(CONNECTION_STRING, DATABASE_NAME, USER_COLLECTION, user)
        if (insertedId != None):
            render_template('profile.html')
        else:
            message = 'Wrong Credentials!!'
    else:
        return render_template('login.html')

@app.route('/forgotpassword', methods=["GET", "POST"])
def forgotpassword():
    if request.method == "GET":
        email = request.form["email"]
        query = { "Email": email }
        user = selectDocuments(CONNECTION_STRING, DATABASE_NAME, USER_COLLECTION, query)
        email = user['Email']

        subject = 'Medics Reset Password Verfication'
        body = 'use the following code ' + uuid.uuid4() + ' to verify your account.'
        sendEmail(email, subject, body, HOST_EMAIL, HOST_EMAILPASSWORD)
    elif request.method == "POST":
        storedVerificationCode = request.form["storedverificationcode"]
        inputVerificationCode = request.form["inputverificationcode"]
        if (storedVerificationCode == inputVerificationCode):
            email = request.form["email"]
            newPassword = request.form["newpassword"]
            query = { "Email": email }
            user = { "Password": newPassword }
            insertedId = updateDocument(CONNECTION_STRING, DATABASE_NAME, USER_COLLECTION, query, user)
            if (insertedId != None):
                message = 'Password updated successfully!!'
            else:
                message = 'Error has been occurred, Please try again!!'
    
@app.route('/profile', methods=["GET", "POST"])
def profile():
    if request.method == "GET":
        query = { "UserName": userName }
        user = selectDocuments(CONNECTION_STRING, DATABASE_NAME, USER_COLLECTION, query)
    elif request.method == "POST":
        userName = session.get("name")
        password = request.form["password"]
        email = request.form["email"]
        fullName = request.form["fullname"]
        bio = request.form["bio"]
        if request.files['file'].filename != '':
            filePath = request.files['file'].filename
            fileId = uploadFile(CONNECTION_STRING, DATABASE_NAME, filePath)
        else:
            fileId = None

        query = { "UserName": userName }
        user = { "UserName": userName, "Password": password, "Email": email, "FullName": fullName, "Bio": bio, "file": fileId }
        insertedId = updateDocument(CONNECTION_STRING, DATABASE_NAME, USER_COLLECTION, query, user)
        if (insertedId != None):
            message = 'User updated successfully!!'
        else:
            message = 'Error has been occurred, Please try again!!'
    
@app.route('/consult', methods=["GET", "POST"])
def consult():
    if request.method == "POST":
        if session.get("name"):
            userName = session.get("name")
        message = request.form["message"]
        consultationId = request.form["consultationid"]

        if (consultationId != None or consultationId != ''):
            consultation = { "UserName": userName, "TimeStamp": time.time() }
            consultationId = insertDocument(CONNECTION_STRING, DATABASE_NAME, USER_COLLECTION, consultation)

        query = { "Id": consultation }
        consultation = {"Messages": [{"UserName" : userName, "Content" : message}]}
        insertedId = insertSubdocuments(CONNECTION_STRING, DATABASE_NAME, USER_COLLECTION, query, consultation)
        if (insertedId != None):
            message = 'Consultation submitted successfully!!'
        else:
            message = 'Error has been occurred, Please try again!!'

@app.route('/consultation', methods=["GET", "POST"])
def consultation():
    if request.method == "GET":
        consultationId = request.form["consultationid"]

        if (consultationId != None or consultationId != ''):
            query = { "Id": consultationId }
            consultation = selectDocuments(CONNECTION_STRING, DATABASE_NAME, USER_COLLECTION, query)

@app.route('/consultations', methods=["GET", "POST"])
def consultations():
    if request.method == "GET":
        if session.get("name"):
            userName = session.get("name")
            
            query = { "UserName": userName }
            consultation = selectDocuments(CONNECTION_STRING, DATABASE_NAME, USER_COLLECTION, query)


if __name__ == '__main__':
    app.run(debug=True)
