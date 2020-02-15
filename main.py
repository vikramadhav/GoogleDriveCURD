# Essential Import
from __future__ import print_function
import os
import io

# Local Import
import Authentication.Auth
from Operations.FolderOperation import FolderOperation
from Operations.CustomApiClient import CustomApiClient
from Operations.Files import FilesOperation
import json

# Open the JSOn configuration file and Fetch Data
with open(os.path.join(os.getcwd(),'config.json')) as config_file:
    data = json.load(config_file)


# Build Client Dependencies
myclient = CustomApiClient(data)
folderoperation = FolderOperation(myclient.drive_service)
fileOperation = FilesOperation(myclient.drive_service)


def main():
        parentFolderid = None
        folderoperation.EmptyTrash()
        parentfolder = folderoperation.create(data['FolderName'])
        if parentfolder:
            parentFolderid = parentfolder[0].get('id')

        localCopies = folderoperation.getLocalFolder(data['LocalFolder'])
        for key, value in localCopies.items():
           if fileOperation.uploadFile(value, parentFolderid):
                fileOperation.moveFileToFolder(value, f"{data['AfterCopyFolder']}\\{key}")

if __name__ == '__main__':
    main()
