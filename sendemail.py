import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from http.server import BaseHTTPRequestHandler, HTTPServer
IPadd = "192.168.43.46"

turn_on = IPadd + ':8080/on'
turn_off = IPadd + ':8080/off'
print('Sending EMAIL...!')
email_sender = 'jakrota2021@gmail.com'
email_receiver = 'kpmhp2206@gmail.com'
subject = ''
msg = MIMEMultipart()
msg['From'] = email_sender
msg['To'] = email_receiver
msg['Subject']= subject
body  = "This email is sent by python code \n\n" + turn_on + "\n\n" + turn_off
msg.attach(MIMEText(body, 'plain'))

#FILE PART

#########

text = msg.as_string()
connection = smtplib.SMTP('smtp.gmail.com', 587)
connection.starttls()
connection.login(email_sender, 'jakrota@bepb2021')
connection.sendmail(email_sender, email_receiver, text )
connection.quit()
print('EMAIL sent!')

Request = None

class RequestHandler_httpd(BaseHTTPRequestHandler):
  def do_GET(self):
    global Request
    
    
    Request = self.requestline
    Request = Request[5 : int(len(Request)-9)]
    print(Request)
    if Request == 'off':
      messagetosend = bytes('link 2 is selected',"utf")
      print('command 2 is sent by owner')
    if Request == 'on':
      messagetosend = bytes('link 1 is selected',"utf")
      print('command 1 is sent by owner')
    self.send_response(200)
    self.send_header('Content-Type', 'text/plain')
    self.send_header('Content-Length', len(messagetosend))
    self.end_headers()
    self.wfile.write(messagetosend)
    return


server_address_httpd = (IPadd,8080)
httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
print('Server starting...')
httpd.serve_forever()