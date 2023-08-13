import emails

def sendEmail(receiverEmail, emailSubject, emailBody, senderEmailAddress, senderEmailPassword, senderEmailTitle, hostServer='smtp.gmail.com', hostPort=587, tls=True, timeout=10):
    message = emails.html(html = emailBody,                                         
                          subject = emailSubject,                                           
                          mail_from = (senderEmailTitle, senderEmailAddress)) # Sender Details

    mail = message.send(to=receiverEmail, 
                        smtp={'host': hostServer,            
                              'timeout': timeout,
                              'port': hostPort,
                              'user': senderEmailAddress,    
                              'password': senderEmailPassword,    
                              'tls': tls})  
    
    # Return value based on sending success
    status = False
    if mail.status_code == 250:
        status = True
    else:
        status = False
    
    return status

# Test:
# result = sendEmail('ahmedfahmyaee@yahoo.com', 'test1', 'message1', 'enterprisse.technology@gmail.com', 'yzjyuxgmedtmiwqv', 'Enterprisse Technology')
# print(result)


