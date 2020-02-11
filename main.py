# Essential Import
from __future__ import print_function
import os
import io

# From Drive Operations Specific
from oauth2client import tools

#Local Import
import Authentication.Auth
from Operations.FolderOperation import FolderOperation
from Operations.CustomApiClient import CustomApiClient
import json

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

## Open the JSOn configuration file and Fetch Data
with open('config.json') as config_file:
    data = json.load(config_file)


## Build Client Dependencies 
myclient=CustomApiClient(data)
folderoperation = FolderOperation(myclient.drive_service)

def main():
    folderoperation.create(data['FolderName'])
    folderoperation.listFolder(data['FolderName'])
    folderoperation.removeFolder(folderName=data['FolderName'])
    folderoperation.EmptyTrash()

if __name__ == '__main__':
    main()
