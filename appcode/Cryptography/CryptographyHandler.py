import hashlib
import os 

# ------------------------------------------------------------------------------------------
# MD5 HASH Algorithm:
# ------------------------------------------------------------------------------------------

def hash(string):
    # Encode clear string using encode() then send to md5()
    hashResult = hashlib.md5(string.encode())
    # Get the equivalent hexadecimal value of hash
    hexhashResult = hashResult.hexdigest()
    
    # Return value
    return hexhashResult

def compareHash(string, hash):
    # Encode clear string using encode() then send to md5()
    stringHash = hashlib.md5(string.encode())
    # Get the equivalent hexadecimal value of hash
    stringHexhash = stringHash.hexdigest()
    
    # Compare newly hashed string to given hash
    status = False
    if (hash == stringHexhash):
        status = True
    
    # Return value based on comparison process
    return status

# ------------------------------------------------------------------------------------------
# AES Algorithm:
# ------------------------------------------------------------------------------------------

def encrypt(clearData, key = None, iv = None):
    import Cryptography.AES as AES, os
    
    # Convert string to bytes to pass to algorithm
    clearDataBytes = bytes(clearData, 'utf-8') 
   
    # Generate key and iv if not supplied
    gkey = key
    giv = iv
    if (key is None):
        gkey = os.urandom(16)
    if (key is None):
        giv = os.urandom(16)
    
    # Encrypt clear data 
    cipherData = AES.AES(gkey).encrypt_ctr(clearDataBytes, giv)
    
    # Compose a dictionary of generated key, value and returned ciphered data
    result = {'key': gkey, 'iv': giv, 'data': cipherData}
    
    # Return value
    return result

def decrypt(cipherData, key, iv):
    import Cryptography.AES as AES, os
    
    # Decrypt cipher data
    plainData = AES.AES(key).decrypt_ctr(cipherData, iv)
    
    # Return value
    return plainData

# Test:
# hash("Ahmed")
# x = compareHash("Ahmed", "7f1e43d880f09c64ac6378af6de47702")
# # Generate key and iv
# key = os.urandom(16)
# iv = os.urandom(16)
# result = encrypt('ahmed', key, iv)
# result = encrypt('ahmed')
# result = decrypt(result["data"], result["key"], result["iv"])