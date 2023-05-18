from __future__ import print_function

import os.path
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from pprint import pprint
import base64
from bs4 import BeautifulSoup

from settings import TRASH_LABEL, SCOPES, GMAIL_CREDENTIALS_FILE, GMAIL_ACCESS_TOKEN_FILE



# If modifying scopes, delete the file token.json.


def get_new_trashmails(service):
    all_mails = service.users().messages().list(userId='me').execute()
    new_mails = []

    for mailobj in all_mails['messages']:
        mail_id = mailobj['id']
        mail = service.users().messages().get(userId='me', id=mail_id, format="full").execute()
        labels = mail['labelIds']

        # if unread and label is correct 'Trashbot' label, get content
        if all(x in labels for x in ['UNREAD', TRASH_LABEL]):
            s = mail["payload"]["body"]["data"]
            mail_content = ""
            mail_content += str(base64.urlsafe_b64decode(s + '=' * (4 - len(s) % 4)).decode('utf-8'))
            split_mail = mail_content.split("\r\n\r\n")
            message = "Hallo ihr Lieben!\nDie nächste Müllabfuhr steht an:\n" + split_mail [1]
            new_mails.append(message)

            # mark as read
            mark_as_read = {"removeLabelIds": ["UNREAD"]}
            service.users().messages().modify(userId='me', id=mail_id, body=mark_as_read).execute()
    return new_mails


def authenticate():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(GMAIL_ACCESS_TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(GMAIL_ACCESS_TOKEN_FILE, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                GMAIL_CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(GMAIL_ACCESS_TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        return service
    except HttpError as error:
        print(f'An error occurred: {error}')