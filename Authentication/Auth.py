from __future__ import print_function
import pickle
import os.path
from Utilities import *
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import google.auth.exceptions


class Auth:
    def __init__(self, SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME):
        self.SCOPES = SCOPES
        self.CLIENT_SECRET_FILE = CLIENT_SECRET_FILE
        self.APPLICATION_NAME = APPLICATION_NAME
        self.args = getArguments()
        self.args.noauth_local_webserver = True
       

    def getCredentials(self):

        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.

        creds = None

        try:
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    creds = pickle.load(token)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', self.SCOPES,redirect_uri='urn:ietf:wg:oauth:2.0:oob')
                    auth_url, _ = flow.authorization_url(prompt='consent')
                    print('Please go to this URL: {}'.format(auth_url))
                    # The user will get an authorization code. This code is used to get the
                    # access token.
                    code = input('Enter the authorization code: ')
                    token=flow.fetch_token(code=code)
                    print(token)
                    creds=flow.credentials
                # Save the credentials for the next run
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
            return creds
        except Exception as ex:
            print(ex)
            if ex.__class__ == google.auth.exceptions.RefreshError:
                if os.path.exists('token.pickle'):
                    os.remove('token.pickle')
                    
            else:
                return None
