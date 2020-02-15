from __future__ import print_function

import httplib2
from Authentication.Auth import Auth
from googleapiclient.discovery import build


class CustomApiClient:
    def __init__(self,data):
        authInst = Auth(data["Scopes"], data["Client_Secret_File"], data["Application_Name"])
        credentials= authInst.getCredentials()
        self.drive_service= build('drive', 'v3', credentials=credentials)


   

    def get_driveClient(self):
        return self.drive_service 
        
    property(get_driveClient)