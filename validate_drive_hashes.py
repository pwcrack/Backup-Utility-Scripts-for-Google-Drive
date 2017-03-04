#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import httplib2
import os, sys, hashlib, smtplib
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from operator import itemgetter, attrgetter, methodcaller
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
CLIENT_SECRET_FILE = 'vdh_client_secret.json'
APPLICATION_NAME = 'Validate Drive Hashes'


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
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http)

    remote = []
    results = service.files().list(maxResults=1000, q="trashed=false", fields="items(originalFilename,md5Checksum)").execute()
    items = results.get('items', [])
    remoteitems = sorted(items, key=itemgetter('originalFilename'))
    if not remoteitems:
        print('No files found.')
    else:
        for item in (remoteitems):
            #print('{0},{1}'.format(item['originalFilename'], item['md5Checksum'].upper()))
            remote.append('{0},{1}'.format(item['originalFilename'], item['md5Checksum'].upper()))
    print(remote)
            
    local = []
    for root, dirs, files in os.walk("F:\\GoogleDrive\\"):
        for f in files:
            current_file = os.path.join(root,f)
            localname = f
            localhash = generate_file_md5(current_file)
            local.append('{0},{1}'.format(localname, localhash.upper()))
    local.sort()
    print(local)

    if remote == local:
        fromaddr = "YOUR_GMAIL_ADDRESS@gmail.com"
        toaddr = ["SOME_GMAIL_ADDRESS@gmail.com", "SOME_OTHER_EMAIL_ADDRESS"]
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = ", ".join(toaddr)
        msg['Subject'] = "Google Drive Files Validated"

        body = ""
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "YOUR_GMAIL_ACCOUNT_PASSWORD")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        
    else:
        fromaddr = "YOUR_GMAIL_ADDRESS@gmail.com"
        toaddr = ["SOME_GMAIL_ADDRESS@gmail.com", "SOME_OTHER_EMAIL_ADDRESS"]
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = ", ".join(toaddr)
        msg['Subject'] = "Google Drive Files Failed Validation"

        body = ""
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "YOUR_GMAIL_ACCOUNT_PASSWORD"))
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()

def generate_file_md5(filename, blocksize=2**20):
    m = hashlib.md5()
    with open(filename, "rb" ) as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()

if __name__ == '__main__':
    main()