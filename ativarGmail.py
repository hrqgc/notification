import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    creds =None

    if os.path.exists('credentials/gmail_token.json'):
        creds = Credentials.from_authorized_user_file('credentials/gmail_token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials/client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('credentials/token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)


    request_body = {
        "topicName": "projects/civil-tube-501812-q1/topics/heythere",
        "labelIds":["INBOX"]
    }

    response = service.users().watch(userId='me',body = request_body).execute()
    print(response)
if __name__ == '__main__':
    main()
