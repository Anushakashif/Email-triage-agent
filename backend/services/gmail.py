import os
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, '..', 'credentials.json')
TOKEN_PATH = os.path.join(BASE_DIR, '..', 'token.json')

def get_gmail_service():
    """Authenticate and return Gmail service."""
    creds = None

    # Load existing token if it exists
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    # If no valid credentials, login via browser
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=8080, redirect_uri_trailing_slash=True)

        # Save token for next time
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


def fetch_unread_emails(max_results=20):
    """Fetch last 20 unread emails from Gmail."""
    service = get_gmail_service()

    results = service.users().messages().list(
        userId='me',
        q='is:unread',
        maxResults=max_results
    ).execute()

    emails = []
    for msg in results.get('messages', []):
        detail = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='full'
        ).execute()

        headers = {h['name']: h['value'] for h in detail['payload']['headers']}

        emails.append({
            'id': msg['id'],
            'subject': headers.get('Subject', ''),
            'from': headers.get('From', ''),
            'snippet': detail.get('snippet', '')
        })

    return emails