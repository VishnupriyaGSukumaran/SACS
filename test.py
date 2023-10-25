from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly','https://www.googleapis.com/auth/drive.file']

creds = None

def drive_login():
    global creds
    # If existing token
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

def drive_list():
    global creds
    try:
        drive_service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        results = drive_service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')

def drive_upload():
    drive_service = build('drive', 'v3', credentials=creds)
    file_metadata = {
    'name': 'sample.txt',
    'mimeType': '*/*'
    }
    media = MediaFileUpload('sample.txt',
                            mimetype='*/*',
                            resumable=True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print ('File ID: ' + file.get('id'))


if __name__ == '__main__':
    print('Logging in...')
    drive_login()
    print('Retrieving files in drive...')
    drive_list()
    print('Uploading file sample.txt')
    drive_upload()
    print('Retrieving files in drive...')
    drive_list()