from flask import Flask
from MongoDB.MongoHandler import *
from Cryptography.CryptographyHandler import *
from Messaging.EmailHandler import *
from Messaging.SMSHandler import *

app = Flask(__name__)

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# START: Methods:
# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------

@app.route("/info")
def info():
    return "API to perform all abstract operations"

# ------------------------------------------------------------------------------------------
# Cryptography: MD5 HASH Algorithm:
# ------------------------------------------------------------------------------------------

@app.route("/hash/<clearData>")
def hash(clearData):
    return hash(clearData)

@app.route("/compareHash/<clearData>/<hashData>")
def compareHash(clearData, hashData):
    return compareHash(clearData, hashData)

# ------------------------------------------------------------------------------------------
# Cryptography: AES Algorithm:
# ------------------------------------------------------------------------------------------

@app.route("/encrypt/<clearData>/<key>/<iv>")
@app.route("/encrypt/<clearData>/")
def encrypt(clearData, key = "non", iv = "non"):
    # Reassign parameters deafult values
    if(key == "non"): 
        key = None
    if(iv == "non"): 
        iv = None
    return encrypt(clearData, key, iv)

@app.route("/decrypt/<cipherData>/<key>/<iv>")
def decrypt(cipherData, key, iv):
    return decrypt(cipherData, key, iv)

# ------------------------------------------------------------------------------------------
# Messaging: Email:
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
# Messaging: SMS:
# ------------------------------------------------------------------------------------------

@app.route("/sendSMS/<message>/<receiverNumber>/<senderNumber>/<accountSid>/authToken>")
def sendSMS(message, receiverNumber, senderNumber, accountSid, authToken):
    return sendSMS(message, receiverNumber, senderNumber, accountSid, authToken)

# ------------------------------------------------------------------------------------------
# MongoDB: Check database and collections:
# ------------------------------------------------------------------------------------------

@app.route("/checkIfDatabaseExists/<connectionString>/<databaseName>")
def checkIfDatabaseExists(connectionString, databaseName):
    return checkIfDatabaseExists(connectionString, databaseName)

@app.route("/checkDatabases/<connectionString>")
def checkDatabases(connectionString):
    return checkDatabases(connectionString)

@app.route("/checkIfCollectionExists/<connectionString>/<databaseName>/<collectionName>")
def checkIfCollectionExists(connectionString, databaseName, collectionName):
    return checkIfCollectionExists(connectionString, databaseName, collectionName)

@app.route("/checkCollections/<connectionString>/<databaseName>")
def checkCollections(connectionString, databaseName):
    return checkCollections(connectionString, databaseName)

# ------------------------------------------------------------------------------------------
# MongoDB: Insert:
# ------------------------------------------------------------------------------------------

@app.route("/insertDocument/<connectionString>/<databaseName>/<collectionName>/<document>")
def insertDocument(connectionString, databaseName, collectionName, document):
    return insertDocument(connectionString, databaseName, collectionName, document)

@app.route("/insertDocuments/<connectionString>/<databaseName>/<collectionName>/<documents>")
def insertDocuments(connectionString, databaseName, collectionName, documents):
    return insertDocuments(connectionString, databaseName, collectionName, documents)

@app.route("/insertSubdocuments/<connectionString>/<databaseName>/<collectionName>/<query>/<documents>")
def insertSubdocuments(connectionString, databaseName, collectionName, query, documents):
    return insertSubdocuments(connectionString, databaseName, collectionName, query, documents)

# ------------------------------------------------------------------------------------------
# MongoDB: Update:
# ------------------------------------------------------------------------------------------

@app.route("/updateDocument/<connectionString>/<databaseName>/<collectionName>/<query>/<newData>")
def updateDocument(connectionString, databaseName, collectionName, query, newData):
    return updateDocument(connectionString, databaseName, collectionName, query, newData)

@app.route("/updateDocuments/<connectionString>/<databaseName>/<collectionName>/<query>/<newData>")
def updateDocuments(connectionString, databaseName, collectionName, query, newData):
    return updateDocuments(connectionString, databaseName, collectionName, query, newData)

# ------------------------------------------------------------------------------------------
# MongoDB: Delete:
# ------------------------------------------------------------------------------------------

@app.route("/deleteDocument/<connectionString>/<databaseName>/<collectionName>/<query>")
def deleteDocument(connectionString, databaseName, collectionName, query):
    return deleteDocument(connectionString, databaseName, collectionName, query)

@app.route("/deleteDocuments/<connectionString>/<databaseName>/<collectionName>/<query>")
def deleteDocuments(connectionString, databaseName, collectionName, query):
    return deleteDocuments(connectionString, databaseName, collectionName, query)

@app.route("/deleteSubdocuments/<connectionString>/<databaseName>/<collectionName>/<query>/<subquery>")
def deleteSubdocuments(connectionString, databaseName, collectionName, query, subquery):
    return deleteSubdocuments(connectionString, databaseName, collectionName, query, subquery)

@app.route("/deleteCollection/<connectionString>/<databaseName>/<collectionName>")
def deleteCollection(connectionString, databaseName, collectionName):
    return deleteCollection(connectionString, databaseName, collectionName)

# ------------------------------------------------------------------------------------------
# MongoDB: Select:
# ------------------------------------------------------------------------------------------

@app.route("/selectDocuments/<connectionString>/<databaseName>/<collectionName>/<query>/<fields>/<sortField>/<sortDirection>/<recordsLimit>")
@app.route("/selectDocuments/<connectionString>/<databaseName>/<collectionName>/<query>/<fields>/<sortField>/<sortDirection>")
@app.route("/selectDocuments/<connectionString>/<databaseName>/<collectionName>/<query>/<fields>/<sortField>")
@app.route("/selectDocuments/<connectionString>/<databaseName>/<collectionName>/<query>/<fields>")
@app.route("/selectDocuments/<connectionString>/<databaseName>/<collectionName>/<query>")
@app.route("/selectDocuments/<connectionString>/<databaseName>/<collectionName>")
def selectDocuments(connectionString, databaseName, collectionName, 
                    query = "non", fields = "non", 
                    sortField = "non", sortDirection = "non", 
                    recordsLimit = "non"):
    # Reassign parameters deafult values
    if(query == "non"): 
        query = None
    if(fields == "non"): 
        fields = None
    if(sortField == "non"): 
        sortField = None
    if(sortDirection == "non"): 
        sortDirection = 1
    if(recordsLimit == "non"): 
        recordsLimit = None
         
    return selectDocuments(connectionString, databaseName, collectionName, 
                           query, fields, 
                           sortField, sortDirection, 
                           recordsLimit)

# ------------------------------------------------------------------------------------------
# MongoDB: Files:
# ------------------------------------------------------------------------------------------

@app.route("/uploadFile/<connectionString>/<databaseName>/<filePath>")
def uploadFile(connectionString, databaseName, filePath):
    return uploadFile(connectionString, databaseName, filePath)

@app.route("/downloadFile/<connectionString>/<databaseName>/<filePath>")
def downloadFile(connectionString, databaseName, filePath):
    downloadFile(connectionString, databaseName, filePath)

@app.route("/readFile/<connectionString>/<databaseName>/<fileName>")
def readFile(connectionString, databaseName, fileName):
    return readFile(connectionString, databaseName, fileName)

@app.route("/checkFiles/<connectionString>/<databaseName>")
def checkFiles(connectionString, databaseName):
    return checkFiles(connectionString, databaseName)

@app.route("/checkIfFileExists/<connectionString>/<databaseName>/<fileName>")
def checkIfFileExists(connectionString, databaseName, fileName):
    return checkIfFileExists(connectionString, databaseName, fileName)

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# END: Methods:
# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------

if (__name__=="__main__"):
    app.run()