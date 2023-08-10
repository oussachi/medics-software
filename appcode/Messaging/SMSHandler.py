import os
from twilio.rest import Client

def sendSMS(message, receiverNumber, senderNumber, accountSid, authToken):
    client = Client(accountSid, authToken)
    
    message = client.messages \
        .create(
             body = message,
             from_ = senderNumber,
             to = receiverNumber
         )
    
    return message.sid