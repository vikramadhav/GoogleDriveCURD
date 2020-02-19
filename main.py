# Essential Import
from __future__ import print_function
import os
import io
import sys


# Local Import
from Utilities import *
import Authentication.Auth
from Operations.FolderOperation import FolderOperation
from Operations.CustomApiClient import CustomApiClient
from Operations.Files import FilesOperation


# Build Client Dependencies
class Initiator:
    _parentId = None

    def __init__(self):
        self.myclient = CustomApiClient(data)
        self.folderoperation = FolderOperation(self.myclient.drive_service)
        self.fileOperation = FilesOperation(self.myclient.drive_service)

    def get_ParentId(self):
        return self._parentId

    def set_ParentId(self, value):
        self._parentId = value

    property(get_ParentId, set_ParentId)

    def __execute(self):
        parentFolderid = None
        args = getArguments()
        self.folderoperation.EmptyTrash()
        parentfolder = self.folderoperation.create(data['FolderName'])
        if parentfolder:
            self.set_ParentId(parentfolder[0].get('id'))

        if int(args.runType) == 1:
            self.__downloadLogic()
        else:
            self.__uploadLogic()

    def __downloadLogic(self):
         # Download Files
        fileList = self.fileOperation.listFiles(
            parentid=self.get_ParentId(), size=100)
        for file in fileList:
            if self.fileOperation.downloadFile(file['id'], file['name']):
                    # Delete After download
                self.fileOperation.deleteFile(file['id'], file['name'])

    def __uploadLogic(self):
        localCopies = self.folderoperation.getLocalFolder(
            data['LocalFolder'])
        for key, value in localCopies.items():
            if self.fileOperation.uploadFile(value, self.get_ParentId()):
                self.fileOperation.moveFileToFolder(
                    value, f"{data['AfterCopyFolder']}\\{key}")

    def main(self):
        Initiator.__execute(self)


if __name__ == '__main__':
    obj = Initiator()
    obj.main()
