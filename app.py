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
CONSULTATION_COLLECTION = 'consultations'
HOST_EMAIL = 'medicssoftware@gmail.com'
HOST_EMAILPASSWORD = 'flasktaskupwork'
UPLOAD_FOLDER = './static'

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def home():
    return render_template('user/profile.html')



# DONE
@app.route('/signup', methods=["GET", "POST"])
def signup():
    try:
        if request.method == "POST":

            basedir = os.path.abspath(os.path.dirname(__file__))
            
            userName = request.form["username"]
            password = request.form["password"]
            email = request.form["email"]
            fullName = request.form["fullname"]
            bio = request.form["bio"]
            file = request.files['file']
            filePath = os.path.join(basedir, UPLOAD_FOLDER, file.filename)
            if file.filename != '':
                #filePath = request.files['file'].filename
                file.save(filePath)
                fileId = uploadFile(CONNECTION_STRING, DATABASE_NAME, filePath)
                os.remove(filePath)
            else:
                fileId = None
            query = { "UserName": userName }
            user = { "UserName": userName, "Password": password, "Email": email, "FullName": fullName, "Bio": bio, "file": fileId }
            insertedId = insertDocument(CONNECTION_STRING, DATABASE_NAME, USER_COLLECTION, user)
            if (insertedId != None):
                session['name'] = userName
                message = 'User created successfully!!'
            else:
                message = 'Error has been occurred, Please try again!!'
            return message
        
        else:
            return render_template('user/signup.html')
    except Exception as e:
        return f"error : {e}"


# DONE
@app.route('/signin', methods=["GET", "POST"])
def signin():
    try:
        if request.method == "POST":
            userName = request.form["username"]
            password = request.form["password"]

            user = { "UserName": userName, "Password": password }
            insertedId = selectDocuments(CONNECTION_STRING, DATABASE_NAME, USER_COLLECTION, user)
            insertedIdList = list(insertedId)
            if (len(insertedIdList) != 0):
                session['name'] = userName
                return render_template('user/profile.html')
            else:
                message = 'Wrong Credentials!!'
                return message
        else:
            return render_template('user/signin.html')
    except Exception as e:
        return f'error : {e}'


# TO DO
@app.route('/forgotpassword', methods=["GET", "POST"])
def forgotpassword():
    if request.method == "GET":
        email = request.form["email"]
        query = { "Email": email }
        user = selectDocuments(CONNECTION_STRING, DATABASE_NAME, USER_COLLECTION, query)
        user = list(user)[0]
        email = user['Email']

        subject = 'Medics Reset Password Verfication'
        body = 'use the following code ' + str(uuid.uuid4()) + ' to verify your account.'
        title = 'Password reset'
        sendEmail(email, subject, body, HOST_EMAIL, HOST_EMAILPASSWORD, title)
        return 'Email sent successfully'
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
            return message
        return 'An error occured'
    


# DONE
@app.route('/profile', methods=["GET", "POST"])
def profile():
    userName = session.get("name")
    if request.method == "GET":
        query = { "UserName": userName }
        user = selectDocuments(CONNECTION_STRING, DATABASE_NAME, USER_COLLECTION, query)
        user = list(user)[0]
        return render_template('user/update_profile.html', email=user['Email'],
                               username = userName,
                               fullname = user['FullName'],
                               bio = user['Bio'])
    elif request.method == "POST":
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
        return message





# DONE
@app.route('/consult', methods=["GET", "POST"])
def consult():
    try:
        if request.method == "POST":
            if session.get("name"):
                userName = session.get("name")
            message = request.form["message"]
            consultationId = request.form["consultationid"]

            if (consultationId == None or consultationId == ''):
                consultation = { "UserName": userName, "TimeStamp": time.time() }
                consultationId = insertDocument(CONNECTION_STRING, DATABASE_NAME, CONSULTATION_COLLECTION, consultation)
            
            query = { "Id": consultationId }
            consultation = {"Messages": [{"UserName" : userName, "Content" : message}]}
            status = insertSubdocuments(CONNECTION_STRING, DATABASE_NAME, CONSULTATION_COLLECTION, query, consultation)
            if (status):
                message = 'Consultation submitted successfully!!'
            else:
                message = 'Error has been occurred, Please try again!!'
            return message
        else:
            return render_template('user/consult.html')
    except Exception as e:
        return f'error : {e}'





# TO DO
@app.route('/consultation', methods=["GET", "POST"])
def consultation():
    if request.method == "GET":
        consultationId = request.form["consultationid"]

        if (consultationId != None or consultationId != ''):
            query = { "Id": consultationId }
            consultation = selectDocuments(CONNECTION_STRING, DATABASE_NAME, USER_COLLECTION, query)
            return consultation







# DONE
@app.route('/consultations', methods=["GET", "POST"])
def consultations():
    if request.method == "GET":
        if session.get("name"):
            userName = session.get("name")
            
            query = { "UserName": userName }
            consultations = selectDocuments(CONNECTION_STRING, DATABASE_NAME, CONSULTATION_COLLECTION, query)
            consultations = list(consultations)
            return render_template('user/consultations.html', username=userName, consultations=consultations)


if __name__ == '__main__':
    app.run(debug=True)
