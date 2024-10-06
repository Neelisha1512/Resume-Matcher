from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
from googleapiclient.discovery import build
from PyPDF2 import PdfReader

import io
from googleapiclient.http import MediaIoBaseDownload

# If modifying these SCOPES, delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate_google_drive():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens.
    # It is created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    drive_service = build('drive', 'v3', credentials=creds)
    return drive_service

def get_resumes(folder_id):
    drive_service = authenticate_google_drive()
    # Fetch resumes from the specified Google Drive folder
    results = drive_service.files().list(q=f"'{folder_id}' in parents", pageSize=10).execute()
    items = results.get('files', [])
    return items

def download_resume(file_id):
    drive_service = authenticate_google_drive()
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    fh.seek(0)
    return fh

def extract_text_from_pdf(file_content):
    reader = PdfReader(file_content)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file_content):
    document = Document(file_content)
    return '\n'.join([para.text for para in document.paragraphs])
