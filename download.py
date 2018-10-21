# -*- encoding: UTF-8 -*-

import os
import httplib2

# pip install --upgrade google-api-python-client
from oauth2client.file import Storage
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from googleapiclient import http
from io import FileIO
from httplib2 import Http
import sys

# Copy your credentials from the console
# https://console.developers.google.com
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']


OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
OUT_PATH = os.path.join(os.path.dirname(__file__), 'out')
CREDS_FILE = os.path.join(os.path.dirname(__file__), 'credentials.json')

if not os.path.exists(OUT_PATH):
    os.makedirs(OUT_PATH)

storage = Storage(CREDS_FILE)
credentials = storage.get()

if credentials is None:
    # Run through the OAuth flow and retrieve credentials
    flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
    authorize_url = flow.step1_get_authorize_url()
    print 'Go to the following link in your browser: ' + authorize_url
    code = raw_input('Enter verification code: ').strip()
    credentials = flow.step2_exchange(code)
    storage.put(credentials)


# Create an httplib2.Http object and authorize it with our credentials
httpq = credentials.authorize(Http())
drive_service = build('drive', 'v3', http=httpq)
file_id = sys.argv[1]
request = drive_service.files().export_media(fileId=file_id,
                                             mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
fh = FileIO('test.docx', 'wb')
downloader = http.MediaIoBaseDownload(fh, request)
done = False
while done is False:
    status, done = downloader.next_chunk()
    print "Download %d%%." % int(status.progress() * 100)

