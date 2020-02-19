# Essential Import
from __future__ import print_function
import os
import io
import sys
import argparse
import json

# Local Import
import Authentication.Auth
from Operations.FolderOperation import FolderOperation
from Operations.CustomApiClient import CustomApiClient
from Operations.Files import FilesOperation

# Open the JSOn configuration file and Fetch Data
with open(os.path.join(os.getcwd(), 'config.json')) as config_file:
    data = json.load(config_file)

parser = argparse.ArgumentParser()
parser.add_argument('-rt', '--runType',
                    help='Pass Run Type , 1 for Upload versu other options to download and delete',
                    action="store", required=False)


# Build Client Dependencies
class Initiator:
    def __init__(self):
        self.myclient = CustomApiClient(data)
        self.folderoperation = FolderOperation(myclient.drive_service)
        self.fileOperation = FilesOperation(myclient.drive_service)

    def get_ParentId(self):
        return self._parentId

    def set_ParentId(self, value):
        self._parentId = value

    property(get_ParentId, set_ParentId)

    def Execute(self):
        parentFolderid = None
        args = parser.parse_args()
        self.folderoperation.EmptyTrash()
        parentfolder = self.folderoperation.create(data['FolderName'])
        if parentfolder:
            self.set_ParentId = parentfolder[0].get('id')

    def __downloadLogic(self):
         # Download Files
        fileList = self.fileOperation.listFiles(
            parentid=self.parentFolderid, size=100)
        for file in fileList:
            if self.fileOperation.downloadFile(file['id'], file['name']):
                    # Delete After download
                self.fileOperation.deleteFile(file['id'], file['name'])
 # Upload Files

    def __UploadLogic(self):
        localCopies = self.folderoperation.getLocalFolder(
            data['LocalFolder'])
        for key, value in localCopies.items():
            if self.fileOperation.uploadFile(value, self.get_ParentId):
                self.fileOperation.moveFileToFolder(
                    value, f"{data['AfterCopyFolder']}\\{key}")


def main(argv):
    Initiator.Execute()


if __name__ == '__main__':
    main()
