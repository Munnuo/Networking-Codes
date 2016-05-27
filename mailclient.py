# Charles Warr
# Intro To Networking - CS422
# MAil Client Python Programming Assignment

# This program sends an email to the initialized recipient from the
# initialized sender. The email contains the message of whatever msg consist of.


from socket import *
import socket
import ssl
import sys
import base64

msg = "\r\n Enter the body of the message here"
endMsg = "\r\n.\r\n"

username = "enter email username here"
password = "enter email password here"

sender = "<enter sender email here>"
recipient = "<enter recipient email here>"

# Choose a mail server and call its mailserver

mailServer = "smtp.gmail.com"
mailPort = 587


# creating socket for mail client here
try:
    mailSock = socket.socket(AF_INET, SOCK_STREAM)
    print('- Socket created successfully')
except socket.error:
    print('- Failed to create socket')
    sys.exit()

print('- creating the connection to Mail Server')


mailSock.connect((mailServer, mailPort))

print('- Connection established')

recv = mailSock.recv(1024)
print('')
print(recv)
if recv[:3].decode('UTF-8') != '220' :
    print('220 reply not received from server')

heloCommand = 'HELO Alice\r\n'
mailSock.send(heloCommand.encode('UTF-8'))
recv1 = mailSock.recv(1024)
print (recv1)
if recv1[:3].decode('UTF-8') != '250':
    print ('250 reply not received from server.')

# Request an encrypted connection
startTlsCommand = 'STARTTLS\r\n'
mailSock.send(startTlsCommand.encode('UTF-8'))
TLSrecv = mailSock.recv(1024)
print (TLSrecv)
if TLSrecv[:3].decode('UTF-8') != '220':
    print('220 reply not received from server')

# Encrypting the socket
sslMail = ssl.wrap_socket(mailSock)

# Authentication login command and print server response
authCommand = 'AUTH LOGIN\r\n'
sslMail.write(authCommand.encode('UTF-8'))
AUTHrecv = sslMail.read(1024)
print(AUTHrecv)
if AUTHrecv[:3].decode('UTF-8') != '334':
    print('334 reply not received from server')

# send username and print server response
UNencr = base64.b64encode(username.encode('UTF-8'))+ ('\r\n').encode('UTF-8')
sslMail.write(UNencr)
UNrecv = sslMail.read(1024)
print(UNrecv)
if UNrecv[:3].decode('UTF-8') != '334':
    print('334 reply not received from server')

# send password and print server response
PWencr = base64.b64encode(password.encode('UTF-8')) + ('\r\n').encode('UTF-8')
sslMail.write(PWencr)
PWrecv = sslMail.read(1024)
print(PWrecv)
if PWrecv [:3].decode('UTF-8') != '235':
    print('235 reply not received from server')

# Send MAIL FROM command and print server response
mailFromCommand = 'MAIL FROM: ' + sender + '\r\n'
sslMail.write(mailFromCommand.encode('UTF-8'))
recv2 = sslMail.read(1024)
print (recv2)
if recv2[:3].decode('UTF-8') != '250':
    print('250 reply not received from sender.')

# Send RCPT TO command and print server response
rcptToCommand = 'RCPT TO: ' + recipient + '\r\n'
sslMail.write(rcptToCommand.encode('UTF-8'))
recv3 = sslMail.read(1024)
print(recv3)
if recv3[:3].decode('UTF-8') != '250':
    print('250 reply not received from server')

# send DATA command and print server response
dataCommand = 'DATA\r\n'
sslMail.write(dataCommand.encode('UTF-8'))
recv4 = sslMail.read(1024)
print(recv4)
if recv4[:3].decode('UTF-8') != '354':
    print('354 reply not received from server')

# Send message data
sslMail.write(msg.encode('UTF-8'))

# message ends with a single period
sslMail.write(endMsg.encode('UTF-8'))
recv5 = sslMail.read(1024)
print(recv5)
if recv5[:3].decode('UTF-8') != '250':
    print('250 reply not received from server')

# Send QUIT command and get server response.
quitCommand = 'QUIT\r\n'
sslMail.write(quitCommand.encode('UTF-8'))
recv6 = sslMail.read(1024)
print(recv6)
if recv6[:3].decode('UTF-8') != '221':
	print('221 reply not received from server.')

mailSock.close()


