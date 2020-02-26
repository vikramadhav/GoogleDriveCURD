from __future__ import print_function

import httplib2
from Authentication.Auth import Auth
from googleapiclient.discovery import build
import google.auth.exceptions
import threading
import time

class CustomApiClient:
    db_breaker=None

    def __init__(self, data):
        self.data = data
        self.drive_service=None
        self.authInst = Auth(
                self.data["Scopes"], self.data["Client_Secret_File"], self.data["Application_Name"])
        self.initialize() 
        threading.Thread(target=self.maintaince, daemon=True).start()
     
    def get_driveClient(self):
        return self.drive_service   

    #@db_breaker
    def initialize(self):
        try:
            credentials = self.authInst.getCredentials()
            self.drive_service = build('drive', 'v3', credentials=credentials)
           
        except Exception as ex:
            print(ex)
            

    property(get_driveClient)

    def maintaince(self):
        while True:
            time.sleep(300)
            self.initialize()
           


