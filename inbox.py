######## TEXT ###########

import nltk
import random
import string
import sys
import nltk

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from classes_dict import *

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def lem_tokens(tokens):

	lemmer = nltk.stem.WordNetLemmatizer()

	return [lemmer.lemmatize(token) for token in tokens]

def lem_normalize(text):
	return lem_tokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


def my_response(my_dict, user_input, sent_tokens):

	robo_response = ''

	#sent_tokens.append(user_response)
	sent_tokens['user'] = user_input

	sent_tokens_ = []

	for value in sent_tokens:
		sent_tokens_.append(sent_tokens[value])

	# tfidf_vec = TfidfVectorizer(tokenizer = lem_normalize, stop_words='english')
	tfidf_vec = TfidfVectorizer(tokenizer = lem_normalize)

	tfidf = tfidf_vec.fit_transform(sent_tokens_)
	vals = cosine_similarity(tfidf[-1], tfidf)
	idx = vals.argsort()[0][-2]
	flat = vals.flatten()
	flat.sort()
	req_tfidf = flat[-2]
    # print req_tfidf

	error_threshold = 0.1
	if(req_tfidf < error_threshold):
		if len(my_dict['unsure']['response']):
			ans = my_dict['unsure']['response'][0]
			my_dict['unsure']['response'].pop(0)
			return ans
		else:
			return "Text not recognized"
	else:
		for value in sent_tokens:
			match_pattern = sent_tokens_[idx]
			pattern = sent_tokens[value]
			if match_pattern == pattern:
				match_class = value
		if not len(my_dict[match_class]['response']):
			if len(my_dict['unsure']['response']):
				ans = my_dict['unsure']['response'][0]
				my_dict['unsure']['response'].pop(0)
				return ans
			else:
				return "Text not recognized"
		robo_response = my_dict[match_class]['response'][0]
		my_dict[match_class]['response'].pop(0)

		return robo_response

def post_dict(some_dict):

	sent_tokens = {}

	for value in some_dict:
		words = some_dict[value]["pattern"]
		words = ' '.join(words)
		sent_tokens[value] = words
		word_tokens = nltk.word_tokenize(words)

	return sent_tokens, word_tokens



####### MAIL ############



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



def send(name, to_email=None, subject=None, text = ""):

    msg = format_msg(my_name=name, text=text)

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

sent_tokens, word_tokens = post_dict(classes_dict)


######## MAIN ###########
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
        text = my_response(classes_dict, body, sent_tokens)
        response = send(sender_name, to_email=sender_mail, subject = 'Re: '+subject, text = text)
        print(response)
    sleep(5)
# print(search_data)