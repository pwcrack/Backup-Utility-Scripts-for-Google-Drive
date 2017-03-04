#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
CLIENT_SECRET_FILE = 'emptytrash_client_secret.json'
APPLICATION_NAME = 'Empty Trash'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http)
    candidates = findTrashedFiles(service)
    # Handle the bin update delay
    if len(candidates['items']) > 0:
        printSpace(service)
        print("Starting to remove files")
        for item in candidates['items']:
            if 'originalFilename' not in item:
                item['originalFilename'] = item['id']
            print("\tFile %s, has been moved to trash on %s" % (item['originalFilename'], item['modifiedDate']))
            removeFromTrash(service, item['id'], item['originalFilename'])
        print("\tfinished removing all files")
        printSpace(service)
    else:
        print("No files to remove")

def findTrashedFiles(service):
    print("Getting all trashed files")
    result = service.files().list(q="trashed=true").execute()
    print("\tCompleted request")
    return result

def removeFromTrash(service, fileid, filename):
    print("\ttry to remove %s with id %s" % (filename, fileid))
    try:
        result = service.files().delete(fileId=fileid).execute()
    except errors.HttpError as e:
        if e.resp.reason == "Not Found":
            print("\t%s is already removed or doesn't exist" % (filename))
        else:
            print("ERROR:: failed to remove %s returned %s %s" % (filename, e.resp.status, e.resp.reason))

if __name__ == '__main__':
    main()