
import imaplib
import email
import sys
import requests
from datetime import datetime
from email.header import decode_header

from formatting import format_msg
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from time import sleep
host = 'imap.gmail.com'
username = 'i.will.waste.your.time.spamming@gmail.com'
password = 'asdf1234_'



def send_mail(text='Email Body', subject='Re:', from_email='Ron Obvious <ron.obvious@gmail.com>', to_emails=None, html=None):#.format(username)
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



def send(name, to_email=None, subject=None):

    msg = format_msg(my_name=name)

    try:
        send_mail(text=msg, to_emails=[to_email], html=None, subject = subject)
        sent = True
    except:
        sent = False
    return sent




def get_inbox():
    mail = imaplib.IMAP4_SSL(host)
    mail.login(username, password)
    mail.select("inbox")
    _, search_data = mail.search(None, 'UNSEEN')
    my_message = []
    for num in search_data[0].split():
        email_data = {}
        _, data = mail.fetch(num, '(RFC822)')
        # print(data[0])
        _, b = data[0]
        email_message = email.message_from_bytes(b)
        for header in ['subject', 'to', 'from', 'date']:
            # print("{}: {}".format(header, email_message[header]))
            email_data[header] = email_message[header]
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                email_data['body'] = body.decode()
            elif part.get_content_type() == "text/html":
                html_body = part.get_payload(decode=True)
                email_data['html_body'] = html_body.decode()
        my_message.append(email_data)
    return my_message

from bs4 import BeautifulSoup

def dec(mail):


    subject_list = decode_header(mail['subject'])

    sub_list = []
    for subject in subject_list:
        if subject[1]:
            subject = (subject[0].decode(subject[1]))
        elif type(subject[0]) == bytes:
            subject = subject[0].decode('utf-8')
        else:
            subject = subject[0]
        sub_list.append(subject)

    subject = ''.join(sub_list)
    return subject

while True:
    my_inbox = get_inbox()
    if my_inbox:
        subject = dec(my_inbox[0]).replace('Re:', "").lstrip()
        sender_name = BeautifulSoup(my_inbox[0]['from'], "lxml").text.strip()
        sender_mail = my_inbox[0]['from'][ my_inbox[0]['from'].find('<')+1: my_inbox[0]['from'].find('>')]
        body = BeautifulSoup(my_inbox[0]['body'], "lxml").text.split('--')[0].split(">")[0]
        print("subject\n", subject)
        print("mail\n",sender_mail)
        print("name\n",sender_name)
        print("body:\n", body)
        response = send(sender_name, to_email=sender_mail, subject = 'Re: '+subject)
        print(response)
    sleep(5)
# print(search_data)