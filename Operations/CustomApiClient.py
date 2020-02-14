import httplib2
from Authentication.Auth import Auth
from apiclient import discovery


class CustomApiClient:
    def __init__(self,data):
        authInst = Auth(data["Scopes"], data["Client_Secret_File"], data["Application_Name"])
        credentials= authInst.getCredentials()

        self.http= credentials.authorize(httplib2.Http())
        self.http.redirect_codes = set(self.http.redirect_codes)- {308}
        self.drive_service= discovery.build('drive', 'v3', http=self.http)


    def get_httpRequestObject(self):
        return self.http

    def get_driveClient(self):
        return self.drive_service 
        
    property(get_httpRequestObject,get_driveClient)