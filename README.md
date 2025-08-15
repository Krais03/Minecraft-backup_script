# Minecraft Saves Backup Script
A Python script for automatically backing up the Minecraft `saves` folder to Google Drive
---
## Features
- OAuth 2.0 authorization with Google Drive
- Creates folder structure on Google Drive mirroring the local `saves` folder
- Recursive backup of the entire folder including subfolders and files into a timestamped
- Checks if the main backup folder (`Minecraft_saves`) already exists to avoid duplicates
- Colored status messages in the console for better user experience
---
## Requirements
- Python 3.6 or higher
- Python libraries:
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
- Google account with access to Google Drive API
- `credentials.json` file from Google Cloud Console (OAuth client)
---
## Installation
1. Clone the repository:
git clone https://github.com/yourusername/minecraft_saves_backup.git
cd minecraft_saves_backup
2. Install required libraries:
pip install -r requirements.txt
możesz to zrobić w jednym pliku i po angielsku
3. Configure Google API:
- Create a project in the [Google Cloud Console](https://console.cloud.google.com/)
- Enable Google Drive API
- Create OAuth client credentials and download `credentials.json`
- Place `credentials.json` in the project folder (do not commit it to the repository!)
---
## Usage
1. Run the script:
python Script.py
2. On first run, a browser window will open for Google account authorization.
3. The script will create a `Minecraft_saves` folder on your Google Drive (if it doesn’t
4. The local Minecraft `saves` folder will be recursively uploaded into this subfolder.
---
## Notes
- A `token.pickle` file is generated after the first successful login and used for reauth
- Do not share your `credentials.json` or `token.pickle` files publicly.
- The script only creates backup copies and does not delete any files on Google Drive.
---
## License
MIT License
---
This is a simple yet effective script for automating backups of Minecraft saves to the cloud. Feel free to extend it as needed.
