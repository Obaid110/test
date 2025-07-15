from flask import Flask, render_template, request, redirect
import os
import io
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_drive_service():
    creds = None
    if os.path.exists('token.json'):
        with open('token.json', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'wb') as token:
            pickle.dump(creds, token)
    return build('drive', 'v3', credentials=creds)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        service = get_drive_service()
        file_metadata = {'name': file.filename}
        media = MediaIoBaseUpload(file.stream, mimetype=file.content_type)
        uploaded_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        # Make file public
        file_id = uploaded_file.get('id')
        service.permissions().create(fileId=file_id, body={'role': 'reader', 'type': 'anyone'}).execute()
        link = f'https://drive.google.com/file/d/{file_id}/view?usp=sharing'

        return render_template('index.html', link=link)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
