# Essential Import
from __future__ import print_function
import os
import io

# From Drive Operations Specific
from oauth2client import tools

# Local Import
import Authentication.Auth
from Operations.FolderOperation import FolderOperation
from Operations.CustomApiClient import CustomApiClient
from Operations.Files import FilesOperation
import json

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# Open the JSOn configuration file and Fetch Data
with open('config.json') as config_file:
    data = json.load(config_file)


# Build Client Dependencies
myclient = CustomApiClient(data)
folderoperation = FolderOperation(myclient.drive_service)
fileOperation = FilesOperation(myclient.drive_service, myclient.http)


def main():
        parentFolderid = None
        folderoperation.EmptyTrash()
        parentfolder = folderoperation.create(data['FolderName'])
        if parentfolder:
            parentFolderid = parentfolder[0].get('id')

        localCopies = folderoperation.getLocalFolder(data['LocalFolder'])
        for key, value in localCopies.items():
            fileOperation.uploadFile(value, parentFolderid)

        fileOperation.moveFileToFolder(value, f"{data['AfterCopyFolder']}\\{key}")

if __name__ == '__main__':
    main()
