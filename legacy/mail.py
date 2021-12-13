
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials



def create_message(sender, to, message_id, thread_id, subject, message_text):
	message = MIMEText(message_text)
	message['from'] = sender
	message['to'] = to
	message['In-Reply-To'] = message_id
	message['References'] = message_id
	message['subject'] = subject

	return {
		'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode(),
		'threadId':thread_id
	}


def send_message(service, user_id, message):
    message = (service.users().messages().send(userId="me", 
    body=message).execute())
    print('Message Id: %s' % message['id'])
    return message

def send_email(orders):
	SCOPES = 'https://mail.google.com/'
	# credentials = auth.get_user_oauth2_credentials(scopes=SCOPES, 
	# 																	client_id='998730579031-po0v1uf7gkkqtpuf2181upbaitcgrooo.apps.googleusercontent.com', 
	# 																	client_secret='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')
	credentials = Credentials.from_authorized_user_file('creds.json', SCOPES)
	service = discovery.build('gmail','v1', credentials=credentials)
	message_text = orders[0]
	created_message = create_message('th14@gmail.com','th14@gmail.com', 
		subject()[1],subject()[2], subject()[0], message_text)
	send_message(service, 'me', created_message)

send_email(['Msg Received'])