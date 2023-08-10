from flask import Flask
from MongoHandler import *

app = Flask(__name__)

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# START: Methods:
# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------

@app.route("/info")
def info():
    return "API to perform all database and file operations on MongoDB"

# ------------------------------------------------------------------------------------------
# Check database and collections:
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
# Insert:
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
# Update:
# ------------------------------------------------------------------------------------------

@app.route("/updateDocument/<connectionString>/<databaseName>/<collectionName>/<query>/<newData>")
def updateDocument(connectionString, databaseName, collectionName, query, newData):
    return updateDocument(connectionString, databaseName, collectionName, query, newData)

@app.route("/updateDocuments/<connectionString>/<databaseName>/<collectionName>/<query>/<newData>")
def updateDocuments(connectionString, databaseName, collectionName, query, newData):
    return updateDocuments(connectionString, databaseName, collectionName, query, newData)

# ------------------------------------------------------------------------------------------
# Delete:
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
# Select:
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
# Files:
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