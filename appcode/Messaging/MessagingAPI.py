from flask import Flask
from EmailHandler import *
from SMSHandler import *

app = Flask(__name__)

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# START: Methods:
# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------

@app.route("/info")
def info():
    return "API to perform messaging operations through email or SMS"

# ------------------------------------------------------------------------------------------
# Email:
# ------------------------------------------------------------------------------------------

@app.route("/sendEmail/<receiverEmail>/<emailSubject>/<emailBody>/<senderEmailAddress>/<senderEmailPassword>/<senderEmailTitle>/<hostServer>/<hostPort>/<tls>/<timeout>")
@app.route("/sendEmail/<receiverEmail>/<emailSubject>/<emailBody>/<senderEmailAddress>/<senderEmailPassword>/<senderEmailTitle>/<hostServer>/<hostPort>/<tls>")
@app.route("/sendEmail/<receiverEmail>/<emailSubject>/<emailBody>/<senderEmailAddress>/<senderEmailPassword>/<senderEmailTitle>/<hostServer>/<hostPort>")
@app.route("/sendEmail/<receiverEmail>/<emailSubject>/<emailBody>/<senderEmailAddress>/<senderEmailPassword>/<senderEmailTitle>/<hostServer>")
@app.route("/sendEmail/<receiverEmail>/<emailSubject>/<emailBody>/<senderEmailAddress>/<senderEmailPassword>/<senderEmailTitle>")
def sendEmail(receiverEmail, emailSubject, emailBody, senderEmailAddress, senderEmailPassword, senderEmailTitle, hostServer="non", hostPort="non", tls="non", timeout="non"):
    # Reassign parameters deafult values
    if(hostServer == "non"): 
        hostServer ='smtp.gmail.com'
    if(hostPort == "non"): 
        hostPort = 587
    if(tls == "non"): 
        tls = True
    if(timeout == "non"): 
        timeout = 5
    return sendEmail(receiverEmail, emailSubject, emailBody, senderEmailAddress, senderEmailPassword, senderEmailTitle, hostServer, hostPort, tls, timeout)

# ------------------------------------------------------------------------------------------
# SMS:
# ------------------------------------------------------------------------------------------

@app.route("/sendSMS/<message>/<receiverNumber>/<senderNumber>/<accountSid>/authToken>")
def sendSMS(message, receiverNumber, senderNumber, accountSid, authToken):
    return sendSMS(message, receiverNumber, senderNumber, accountSid, authToken)

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# END: Methods:
# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------

if (__name__=="__main__"):
    app.run()