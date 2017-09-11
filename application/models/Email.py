#-*-coding:utf8-*-

from flaskext.mail import Mail
from flask_mail import Message
from application import app
from threading import Thread

mail = Mail(app)

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

def sendmail(recipients, subject, message):
    msg = Message()
    msg.subject = subject
    msg.recipients = recipients
    msg.html = message
    msg.charset = 'utf-8'
    try:
        thread = Thread(target=send_async_email,args=[app,msg])
        thread.start()
    except Exception,e:
        data = {"status": "fail", "error": "send email error"}
        return data
    return True
