from __future__ import print_function
import os
import math
from Utilities import *

class FolderOperation:

    def __init__(self, drive_service):
        self.drive_service = drive_service
        self.folderMimeTYpe = 'application/vnd.google-apps.folder'

    def create(self, name):
        query = f"name='{name}' and mimeType='{self.folderMimeTYpe}'"
        print(f"Making request for {query}")
        results = self.drive_service.files().list(q=query).execute()
        items = results.get('files', [])
        if items:
            print('Found Similiar Name Folders , Skipping Creation ')
            for file in results.get('files', []):
                print('Found file: %s (%s)' %
                      (file.get('name'), file.get('id')))
        else:
            print('No Folder Found by that Name ,Createing New Folder')
            file_metadata = {
                'name': name,
                'mimeType': self.folderMimeTYpe
            }
            file = self.drive_service.files().create(
                body=file_metadata, fields='id').execute()
            print('Folder ID: %s' % file.get('id'))
            items.append(file)
        return items

    def listFolder(self, name=None) -> []:
        page_token = None
        folderlist = []
        query = f"mimeType='{self.folderMimeTYpe}'"

        if name:
            query = (f"{query} and name ='{name}'")

        while True:
            print(f"Making Request with {query} and PageToken:{page_token}")
            response = self.drive_service.files().list(
                q=query, spaces='drive', fields='nextPageToken, files(id,name)',pageToken=page_token).execute()

            for file in response.get('files', []):
                print('Found file: %s (%s)' %
                      (file.get('name'), file.get('id')))
                folderlist.append(file)
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
            print()
        return folderlist

    def removeFolder(self, folderId=None, folderName=None) -> None:
        if not folderId and not folderName:
            print("No Vaild argument Found for deletion ! Aborting")
            return None
        elif folderName:
            folderList = self.listFolder(folderName)
            for ids in folderList:
                self.__removeFolderById(ids['id'])
        else:
            self.__removeFolderById(folderId)

    def __removeFolderById(self, folderId) -> None:
        print(f"Making Delete Folder Request for {folderId}")
        response = self.drive_service.files().delete(fileId=folderId).execute()
        if not response:
            print(f"Folder:{folderId} is deleted sucessfully")
        else:
            print(f"Error: {response}")

    def EmptyTrash(self) -> None:
        print("Cleaning Trash")
        self.drive_service.files().emptyTrash().execute()
        print("Trash Cleaned")

    def getLocalFolder(self, path) -> {}:
        file_paths = {}
        counter = 0
        for root,dire,files in os.walk(path):
            for filename in files:
                # Join the two strings in order to form the full filepath.
                filepath = os.path.join(root, filename)
                file_paths[filename] = filepath  # Add it to the list.
        for fileName in file_paths:
            counter += 1
            absPath = file_paths[fileName]
            print("FileNumber: %s - %s - FileSize: %s MB" %
                  (counter, absPath, round((file_size(absPath)/1024.0)/1024.0, 2)))
        return file_paths
