from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.


from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication.

drive = GoogleDrive(gauth)

# Directory
directory = "books-test"

# Parent Directory path
parent_dir = os.getcwd()

# Path
path = os.path.join(parent_dir, directory)

folder_list = drive.ListFile(
    {'q': "'15P0mhudJLIwYBnZNDpUsL0RevxzQd_gb' in parents and trashed=false"}).GetList()
# for file1 in file_list:
#   print('title: %s, id: %s' % (file1['title'], file1['id']))
mimetypes = {
    # Drive Document files as MS Word files.
    'application/vnd.google-apps.folder': 'application/epub+zip',

    # Drive Sheets files as MS Excel files.
    'application/vnd.google-apps.spreadsheet': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    # etc.
}

# os.mkdir(path)
for folder in folder_list:
    print(folder['title'])
    folders = drive.ListFile({'q': f"'{folder['id']}' in parents and trashed=false"}).GetList()
    for fol in folders:
        folder = drive.ListFile({'q': f"'{fol['id']}' in parents and trashed=false"}).GetList()
        for file in folder:
            # print(file['mimeType'])
            file.GetContentFile(f"books-test/{file['title']}", mimetype='application/epub+zip')


# file1 = drive.CreateFile({'title': 'Hello.txt'})
# file1.Upload() # Upload the file.
# file1.GetContentFile('Hello.txt') # Download file as 'catlove.png'.
# print('title: %s, id: %s' % (file1['title'], file1['id']))
