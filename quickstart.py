from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import os


def download_books():

    gauth = GoogleAuth()
    scope = ['https://www.googleapis.com/auth/drive']
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name('key.json', scope)
    # gauth.DEFAULT_SETTINGS['client_config_file'] = "client_secrets.json"
    # Try to load saved client credentials
    # gauth.LoadServiceConfigSettings()
    # gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        # gauth.Authorize()
        gauth.ServiceAuth()
    # Save the current credentials to a file
    # gauth.SaveCredentialsFile("mycreds.txt")

    drive = GoogleDrive(gauth)

    # Directory
    directory = "books-test"

    # Parent Directory path
    parent_dir = os.getcwd()

    # Path
    path = os.path.join(parent_dir, directory)

    folder_list = drive.ListFile(
        {'q': "'15P0mhudJLIwYBnZNDpUsL0RevxzQd_gb' in parents and trashed=false"}).GetList()

    if not os.path.exists(path):
        os.mkdir(path)

    # Search for files
    # To-do list: automatic remove files after get in database.
    for folder in folder_list:
        folders = drive.ListFile({'q': f"'{folder['id']}' in parents and trashed=false"}).GetList()
        for fol in folders:
            folder = drive.ListFile({'q': f"'{fol['id']}' in parents and trashed=false"}).GetList()
            for file in folder:
                if file['mimeType'] == 'application/epub+zip':
                    if not os.path.exists(f"books-test/{file['title']}"):
                        file.GetContentFile(
                            f"books-test/{file['title']}", mimetype='application/epub+zip')
                        print(f"{file['title']}")
                    else:
                        print(f"{file['title']} already exists.")
                else:
                    print('Error')
