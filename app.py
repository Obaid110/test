from flask import Flask, render_template, request, redirect
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

app = Flask(__name__)

# Google Drive API scope
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Load service account credentials
SERVICE_ACCOUNT_FILE = 'service_account.json'  # Make sure this file is in your project root

def get_drive_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    return service

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
        uploaded_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        # Make file public
        file_id = uploaded_file.get('id')
        service.permissions().create(
            fileId=file_id,
            body={'role': 'reader', 'type': 'anyone'}
        ).execute()
        link = f'https://drive.google.com/file/d/{file_id}/view?usp=sharing'
        return render_template('index.html', link=link)

    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
