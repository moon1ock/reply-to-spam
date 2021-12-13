import sys
import requests
from datetime import datetime

from formatting import format_msg
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# environment variables
username = 'i.will.waste.your.time.spamming@gmail.com'
password = 'asdf1234_'

def send_mail(text='Email Body', subject='Re:  ', from_email='Ron Obvious <ron.obvious@gmail.com>', to_emails=None, html=None):#.format(username)
    assert isinstance(to_emails, list)
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject
    txt_part = MIMEText(text, 'plain')
    msg.attach(txt_part)
    if html != None:
        html_part = MIMEText(html, 'html')
        msg.attach(html_part)
    msg_str = msg.as_string()
    # login to my smtp server
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(from_email, to_emails, msg_str)
    server.quit()



def send(name, to_email=None, subject=None, verbose=False):
    assert to_email != None

    msg = format_msg(my_name=name)
    if verbose:
        print(name, to_email)
    # send the message
    try:
        send_mail(text=msg, to_emails=[to_email], html=None, subject = subject)
        sent = True
    except:
        sent = False
    return sent



if __name__ == "__main__":

    name = 'Elvira'
    if len(sys.argv) > 1:
        name = sys.argv[1]
    email = 'i.will.waste.your.time.spamming@gmail.com'


    if len(sys.argv) > 2:
        email = sys.argv[2]
    response = send(name, to_email=email, subject = 'Re: Business Proposal')
