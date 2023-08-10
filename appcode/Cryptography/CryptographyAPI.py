from flask import Flask
from CryptographyHandler import *

app = Flask(__name__)

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# START: Methods:
# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------

@app.route("/info")
def info():
    return "API to perform cryptography operations"

# ------------------------------------------------------------------------------------------
# MD5 HASH Algorithm:
# ------------------------------------------------------------------------------------------

@app.route("/hash/<string>")
def hash(string):
    return hash(string)

@app.route("/compareHash/<string>/<hash>")
def compareHash(string, hash):
    return compareHash(string, hash)

# ------------------------------------------------------------------------------------------
# AES Algorithm:
# ------------------------------------------------------------------------------------------

@app.route("/encrypt/<cipherData>/<key>/<iv>")
@app.route("/encrypt/<cipherData>/")
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
# ------------------------------------------------------------------------------------------
# END: Methods:
# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------

if (__name__=="__main__"):
    app.run()