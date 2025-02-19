import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    creds = None

    # Load existing token if available
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Authenticate if no valid credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save new token for future use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def create_message(sender, to, subject, body):
    """Creates an email message with proper encoding."""
    message = MIMEText(body, "plain", "utf-8")  # Explicitly set encoding
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}

def send_email_via_gmail(to_email, subject, body):
    """Sends an email via Gmail API."""
    try:
        service = get_gmail_service()
        message = create_message('bhanushakya2004@gmail.com', to_email, subject, body)
        send_message = service.users().messages().send(userId="me", body=message).execute()
        print(f"✅ Email sent successfully to {to_email}")
        return send_message
    except HttpError as error:
        print(f"❌ An error occurred: {error}")
        return None
