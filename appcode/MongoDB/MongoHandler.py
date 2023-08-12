import pymongo
import gridfs
import base64
from bson.objectid import ObjectId

# ------------------------------------------------------------------------------------------
# Check database and collections:
# ------------------------------------------------------------------------------------------

def checkIfDatabaseExists(connectionString, databaseName):
    # Declare variables
    status = False
    
    # Initialize connection
    dbClient = pymongo.MongoClient(connectionString)
    
    # Check if database exists
    dbList = dbClient.list_database_names()
    if databaseName in dbList:
        status = True
    else:
        status = False
    
    # Return value based on check operation
    return status

def checkDatabases(connectionString):
    # Declare variables
    status = False
    
    # Initialize connection
    dbClient = pymongo.MongoClient(connectionString)
    
    # Check if database exists
    dbList = dbClient.list_database_names()
    
    # Return value based on check operation
    return dbList

def checkIfCollectionExists(connectionString, databaseName, collectionName):
    # Declare variables
    status = False
    
    # Initialize connection
    dbClient = pymongo.MongoClient(connectionString)
    
    # Get database
    db = dbClient[databaseName]
    
    # Check if collection exists
    colList = db.list_collection_names()
    if collectionName in colList:
        status = True
    else:
        status = False
    
    # Return value based on check operation
    return status

def checkCollections(connectionString, databaseName):
    # Initialize connection
    dbClient = pymongo.MongoClient(connectionString)
    
    # Get database
    db = dbClient[databaseName]
    
    # Check if collection exists
    colList = db.list_collection_names()

    # Return value based on check operation
    return colList

# ------------------------------------------------------------------------------------------
# Insert:
# ------------------------------------------------------------------------------------------

def insertDocument(connectionString, databaseName, collectionName, document):
    # Initialize connection
    dbClient = pymongo.MongoClient(connectionString)
    
    # Create or get database if exists
    db = dbClient[databaseName]
    
    # Create or get collection if exists
    col = db[collectionName]
    
    # Insert document
    recordId = col.insert_one(document)
    
    # Return inserted records ids
    return recordId.inserted_id

def insertDocuments(connectionString, databaseName, collectionName, documents):
    # Initialize connection
    dbClient = pymongo.MongoClient(connectionString)
    
    # Create or get database if exists
    db = dbClient[databaseName]
    
    # Create or get collection if exists
    col = db[collectionName]
    
    # Insert documents
    records = col.insert_many(documents)
    
    # Return inserted records id
    return records.inserted_ids

def insertSubdocuments(connectionString, databaseName, collectionName, query, documents):
    # Declare variables
    record = False
    updateQyery = {}
    updateData = { "$push": documents }
    _id = None
    
    # Preprocess updateQyery{} parameter
    i = 0
    # Loop through key value pairs
    for key, val in query.items():
        if (key != 'id' and key != '_id' and key != 'Id'): # Check if the query is anything other than object id
            # Check is item value start with "regex:" to determine wether it is a search pattern or plain item value
            prefix = val[0:6].lower()
            if (prefix == "regex:"):
                # If item value starts with "regex:" add it as a key to the dictionary as below to tell python interpreter to search with regex pattern
                updateQyery.update({key: { "$regex": val[6:] }})
            else:
                # It not as value as it is
                updateQyery.update({key:val})
        else: # Check if the query is object id
            _id = val
        i = i+1 
        
    # Initialize connection
    dbClient = pymongo.MongoClient(connectionString)
    
    # Create or get database if exists
    db = dbClient[databaseName]
    
    # Create or get collection if exists
    col = db[collectionName]
    
    # Insert subdocuments
    if (_id != None): # Check if the query is object id
        record = col.update_one({'_id': ObjectId(_id)}, updateData)
    else:
        record = col.update_one(updateQyery, updateData)
        
    # Return value based on update operation success
    if (record != False):
        status = True
    else:
        status = False
    
    # Return value
    return status

# ------------------------------------------------------------------------------------------
# Update:
# ------------------------------------------------------------------------------------------

def updateDocument(connectionString, databaseName, collectionName, query, newData):
    # Declare variables
    record = False
    updateQyery = {}
    updateData = { "$set": newData }
    
    # Preprocess updateQyery{} parameter
    i = 0
    # Loop through key value pairs
    for key, val in query.items():
        # Check is item value start with "regex:" to determine wether it is a search pattern or plain item value
        prefix = val[0:6].lower()
        if (prefix == "regex:"):
            # If item value starts with "regex:" add it as a key to the dictionary as below to tell python interpreter to search with regex pattern
            updateQyery.update({key: { "$regex": val[6:] }})
        else:
            # It not as value as it is
            updateQyery.update({key:val})
        i = i+1
    
    # Initialize connection
    dbClient = pymongo.MongoClient(connectionString)
    
    # Create or get database if exists
    db = dbClient[databaseName]
    
    # Create or get collection if exists
    col = db[collectionName]
    
    # Update document
    record = col.update_one(updateQyery, updateData)
    
    # Return value based on delete operation success
    if (record != False):
        status = True
    else:
        status = False
    
    # Return value
    return status

def updateDocuments(connectionString, databaseName, collectionName, query, newData):
    # Declare variables
    updateQyery = {}
    updateData = { "$set": newData }
    
    # Preprocess updateQyery{} parameter
    i = 0
    # Loop through key value pairs
    for key, val in query.items():
        # Check is item value start with "regex:" to determine wether it is a search pattern or plain item value
        prefix = val[0:6].lower()
        if (prefix == "regex:"):
            # If item value starts with "regex:" add it as a key to the dictionary as below to tell python interpreter to search with regex pattern
            updateQyery.update({key: { "$regex": val[6:] }})
        else:
            # It not as value as it is
            updateQyery.update({key:val})
        i = i+1
    
    # Initialize connection
    dbClient = pymongo.MongoClient(connectionString)
    
    # Create or get database if exists
    db = dbClient[databaseName]
    
    # Create or get collection if exists
    col = db[collectionName]
    
    # Update document
    records = col.update_many(updateQyery, updateData)
    
    # Return modified records count
    return records.modified_count

# ------------------------------------------------------------------------------------------
# Delete:
# ------------------------------------------------------------------------------------------

def deleteDocument(connectionString, databaseName, collectionName, query):
    # Declare variables
    status = False
    deleteQyery = {}
    
    # Preprocess deleteQyery{} parameter
    i = 0
    # Loop through key value pairs
    for key, val in query.items():
        # Check is item value start with "regex:" to determine wether it is a search pattern or plain item value
        prefix = val[0:6].lower()
        if (prefix == "regex:"):
            # If item value starts with "regex:" add it as a key to the dictionary as below to tell python interpreter to search with regex pattern
            deleteQyery.update({key: { "$regex": val[6:] }})
        else:
            # It not as value as it is
            deleteQyery.update({key:val})
        i = i+1
    
    # Initialize connection
    dbClient = pymongo.MongoClient(connectionString)
    
    # Create or get database if exists
    db = dbClient[databaseName]
    
    # Create or get collection if exists
    col = db[collectionName]
    
    # Delete document
    record = col.delete_one(deleteQyery)
    
    # Return value based on delete operation success
    if (record != None):
        status = True
    else:
        status = False
    
    # Return value
    return status

def deleteDocuments(connectionString, databaseName, collectionName, query):
    # Declare variables
    deleteQyery = {}
    
    # Preprocess deleteQyery{} parameter
    i = 0
    # Loop through key value pairs
    for key, val in query.items():
        # Check is item value start with "regex:" to determine wether it is a search pattern or plain item value
        prefix = val[0:6].lower()
        if (prefix == "regex:"):
            # If item value starts with "regex:" add it as a key to the dictionary as below to tell python interpreter to search with regex pattern
            deleteQyery.update({key: { "$regex": val[6:] }})
        else:
            # It not as value as it is
            deleteQyery.update({key:val})
        i = i+1
        
    # Initialize connection
    dbClient = pymongo.MongoClient(connectionString)
    
    # Create or get database if exists
    db = dbClient[databaseName]
    
    # Create or get collection if exists
    col = db[collectionName]
    
    # Delete document
    records = col.delete_many(deleteQyery)
    
    # Return deleted records count
    return records.deleted_count

def deleteSubdocuments(connectionString, databaseName, collectionName, query, subquery):
    # Declare variables
    record = False
    updateQyery = {}
    updateData = { "$pull": subquery }
    
    # Preprocess updateQyery{} parameter
    i = 0
    # Loop through key value pairs
    for key, val in query.items():
        # Check is item value start with "regex:" to determine wether it is a search pattern or plain item value
        prefix = val[0:6].lower()
        if (prefix == "regex:"):
            # If item value starts with "regex:" add it as a key to the dictionary as below to tell python interpreter to search with regex pattern
            updateQyery.update({key: { "$regex": val[6:] }})
        else:
            # It not as value as it is
            updateQyery.update({key:val})
        i = i+1
    
    # Initialize connection
    dbClient = pymongo.MongoClient(connectionString)
    
    # Create or get database if exists
    db = dbClient[databaseName]
    
    # Create or get collection if exists
    col = db[collectionName]
    
    # Update document
    record = col.update_many(updateQyery, updateData)

    # Return value based on delete operation success
    if (record != False):
        status = True
    else:
        status = False
    
    # Return value
    return status

def deleteCollection(connectionString, databaseName, collectionName):
    # Declare variables
    status = False
    
    # Initialize connection
    dbClient = pymongo.MongoClient(connectionString)
    
    # Create or get database if exists
    db = dbClient[databaseName]
    
    # Create or get collection if exists
    col = db[collectionName]
    
    # Delete collection
    record = col.drop()
    
    # Return value based on delete operation success
    if (record != None):
        status = True
    else:
        status = False
        
    # Return deleted collection status
    return status

# ------------------------------------------------------------------------------------------
# Select:
# ------------------------------------------------------------------------------------------

def selectDocuments(connectionString, databaseName, collectionName, 
                    query = None, fields = None, 
                    sortField = None, sortDirection = 1, 
                    recordsLimit = None):
    # Declare variables
    selectQyery = {}
    
    # Preprocess selectQyery{} parameter
    if (query != None):
        i = 0
        # Loop through key value pairs
        for key, val in query.items():
            # Check is item value start with "regex:" to determine wether it is a search pattern or plain item value
            prefix = val[0:6].lower()
            if (prefix == "regex:"):
                # If item value starts with "regex:" add it as a key to the dictionary as below to tell python interpreter to search with regex pattern
                selectQyery.update({key: { "$regex": val[6:] }})
            else:
                # It not as value as it is
                selectQyery.update({key:val})
            i = i+1
        
    # Initialize connection
    dbClient = pymongo.MongoClient(connectionString)
    
    # Create or get database if exists
    db = dbClient[databaseName]
    
    # Create or get collection if exists
    col = db[collectionName]
    
    # Select from document
    if (query != None and fields != None):
        records = col.find(selectQyery, fields)
    elif (query != None and fields == None):
        records = col.find(selectQyery)
    elif (query == None and fields != None):
        records = col.find({}, fields)
    elif (query == None and fields == None):
        records = col.find()
        
    if (sortField != None and sortDirection != None):
        records = records.sort(sortField, sortDirection)
    elif (sortField != None and sortDirection == None):
        records = records.sort(sortField)
    
    if (recordsLimit != None):
        records = records.limit(recordsLimit)
    
    # Return selected records
    return records

# ------------------------------------------------------------------------------------------
# Files:
# ------------------------------------------------------------------------------------------

def uploadFile(connectionString, databaseName, filePath):
    # Initialize connection
    dbClient = pymongo.MongoClient(connectionString)
    
    # Create or get database if exists
    db = dbClient[databaseName]

    # Seperate file path and name
    fileName = filePath[filePath.rfind('/') + 1:]
    fileLocation = filePath[0:filePath.rfind('/') + 1]
    fileFullPath = fileLocation + fileName
    
    # Open file to read
    file_data = open(fileFullPath, "rb")
    # Read file data
    data = file_data.read()
    # Instantiate an object from GridFS
    fs = gridfs.GridFS(db)
    # Upload file into database and return its auto generated id
    fileId = fs.put(data, filename = fileName)
    
    # Return uploaded file is
    return fileId

def downloadFile(connectionString, databaseName, filePath):
    # Initialize connection
    dbClient = pymongo.MongoClient(connectionString)
    
    # Create or get database if exists
    db = dbClient[databaseName]

    # Seperate file path and name
    fileName = filePath[filePath.rfind('/') + 1:]
    fileLocation = filePath[0:filePath.rfind('/') + 1]
    # Compose download full path
    downloadFullPath = fileLocation + fileName
    
    # Find file in database by name
    data = db.fs.files.find_one({'filename':fileName})
    # Retrieve id of the file
    fileId = None
    if data != None:
        fileId = data['_id']
    fileId = data['_id']
    # Instantiate an object from GridFS
    fs = gridfs.GridFS(db)
    # Get file by id to read
    outputdata = fs.get(fileId).read()
    # Open file to write into download path
    output = open(downloadFullPath, "wb")
    # Write file into download path
    output.write(outputdata)
    # Close file writer
    output.close()
    
def readFile(connectionString, databaseName, fileName):
    # Initialize connection
    dbClient = pymongo.MongoClient(connectionString)
    
    # Create or get database if exists
    db = dbClient[databaseName]

    # Find file in database by name
    data = db.fs.files.find_one({'filename':fileName})
    # Retrieve id of the file
    fileId = None
    if data != None:
        fileId = data['_id']
    # Instantiate an object from GridFS
    fs = gridfs.GridFS(db)
    # Get file by id to read
    outputdata = fs.get(fileId).read()
    
    # Convert file into base64 format string
    base64File = base64.b64encode(outputdata)
    
    # Return file base64 string
    return base64File

def checkFiles(connectionString, databaseName):
    # Initialize connection
    dbClient = pymongo.MongoClient(connectionString)
    
    # Create or get database if exists
    db = dbClient[databaseName]

    # Instantiate an object from GridFS
    fs = gridfs.GridFS(db)
    # List all files inside database
    files = fs.list()
    
    # Return file names
    return files

def checkIfFileExists(connectionString, databaseName, fileName):
    # Initialize connection
    dbClient = pymongo.MongoClient(connectionString)
    
    # Create or get database if exists
    db = dbClient[databaseName]

    # Find file in database by name
    data = db.fs.files.find_one({'filename':fileName})
    # Retrieve id of the file
    if data != None:
        fileId = data['_id']
    else:
        fileId = None
    
    # Return file id if exists
    return fileId

