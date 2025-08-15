from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
from datetime import datetime
SCOPES = ['https://www.googleapis.com/auth/drive.file']

creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('drive', 'v3', credentials=creds)

now = datetime.now()
formatted = now.strftime("%m/%d/%Y %H:%M:%S")
print(formatted)

def find_folder(service, folder_name, parent_id=None):
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    folders = results.get('files', [])
    return folders

def create_folder(service, name, parent_id=None):
    metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_id:
        metadata['parents'] = [parent_id]
    print('Creating folder', '\033[94m' + name + '\033[0m' + '\033[92m', end='\r')
    folder = service.files().create(body=metadata, fields='id').execute()
    print('Creating folder', '\033[94m' + name + '\033[0m' + '\033[92m' + ' [Done]' + '\033[0m')
    return folder.get('id')

def upload_file(service, filepath, parent_id):
    file_metadata = {'name': os.path.basename(filepath), 'parents': [parent_id]}
    media = MediaFileUpload(filepath, resumable=True)
    print('Uploading ' '\033[94m' + '{}'.format(os.path.basename(filepath)) + '\033[0m', end='\r')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print('Uploading ' '\033[94m' + '{}'.format(os.path.basename(filepath)) + '\033[0m' + '\033[92m' + ' [Done]' + '\033[0m')
    return file.get('id')

def upload_folder(service, folder_path, parent_id=None):
    folder_name = os.path.basename(folder_path)
    folder_id = create_folder(service, folder_name, parent_id)

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            upload_folder(service, item_path, folder_id)

        else:
            upload_file(service, item_path, folder_id)

folders = find_folder(service, 'Minecraft_saves')
if folders:
    folder = folders[0]
    print('\033[93m' + f'Folder "Minecraft_saves" już istnieje. ID: {folder["id"]}' + '\033[0m')
else:
    file_metadata = {
        'name': 'Minecraft_saves',
        'mimeType': 'application/vnd.google-apps.folder'
    }
    print('\033[96mTworzę folder "Minecraft_saves"...\033[0m', end='\r')
    folder = service.files().create(body=file_metadata).execute()
    print('\033[92mTworzę folder "Minecraft_saves" [Done]\033[0m')

underfile_metadata = {
    'name' : 'Saves | '+formatted,
    'mimeType' : 'application/vnd.google-apps.folder',
    'parents': [folder['id']]
}

under_folder = service.files().create(body=underfile_metadata).execute()
print('Utworzono folder o ID:', folder.get('id'))

upload_folder(service, 'C:/Users/janek/AppData/Roaming/.minecraft/saves', parent_id=under_folder.get('id'))