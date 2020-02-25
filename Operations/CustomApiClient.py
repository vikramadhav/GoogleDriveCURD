from __future__ import print_function

import httplib2
from Authentication.Auth import Auth
from googleapiclient.discovery import build
import google.auth.exceptions



class CustomApiClient:
    db_breaker=None

    def __init__(self, data):
        self.data = data
        

    @db_breaker
    def initialize(self):
        try:
            authInst = Auth(
                self.data["Scopes"], self.data["Client_Secret_File"], self.data["Application_Name"])
            credentials = authInst.getCredentials()
            self.drive_service = build('drive', 'v3', credentials=credentials)
        except Exception as ex:
            print(ex)
            if ex is google.exceptions.DefaultCredentialsError:
                self.initialize()

    def get_driveClient(self):
        return self.drive_service

    property(get_driveClient)
