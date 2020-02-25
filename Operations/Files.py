from __future__ import print_function
import os
import shutil
import io
import json
from Utilities import *
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload


class FilesOperation:
    def __init__(self, drive_service):
        self.drive_service = drive_service
        self.imageMimeType = 'image/jpeg'
        self.UnknownMimeType = 'application/vnd.google-apps.unknown'

    def callback(self, request_id, response, exception):
        if exception:
            print("Exception:", exception)

    def uploadFile(self, filePath, parentid):

        print(f"Uploading File with {filePath}")

        f = open(filePath, "r+")
        fName = os.path.basename(f.name)
        isExist = self.listFiles(1, fileName=fName, parentid=parentid)
        if not isExist:
            file_metadata = {'name': fName, 'title': fName,
                             "parents": [parentid]}

            media = MediaFileUpload(
                filePath, chunksize=1024*1024, resumable=True)

            try:
                file = self.drive_service.files().create(
                    body=file_metadata,  media_body=media, fields='id,name').execute()
                print('File ID: %s with name:%s Uploaded' %
                      (file.get('id'), file.get('name')))
                return True
            except HttpError as err:
                print(err)
                return False
        else:
            print("File Already exist in same folder ! Uploading Aborted")
            return False

    def moveFileToFolder(self, filename, destination):
        print("Moving file %s to %s" % (filename, destination))
        shutil.move(filename, destination)

    def listFiles(self, size, fileName=None, fileId=None, parentid=None):
        query = ''
        page_token = None
        filelist = []
        if not fileId and not fileName and not parentid:
            print("No Valid Parameter are found. Aborting!")
        if parentid:
            query += f"parents in '{parentid}' "

        if fileName:
            if query:
                query += " and "
            query += f"name='{fileName}' "
        elif fileId:
            if query:
                query += " and "
            query += f"id='{fileId}' '"

        query += " and mimeType != 'application/vnd.google-apps.folder' and trashed=false"
        while True:
            print(f"Making Request with {query} and PageToken:{page_token}")
            try:
                response = self.drive_service.files().list(q=query, spaces='drive', pageSize=size,
                                                           fields="nextPageToken,files(id, name)", pageToken=page_token).execute()

                items = response.get('files', [])
                if not items:
                    print('No Files found.')
                    return []
                else:
                    filelist += items
                    print('Files:')
                    for item in items:
                        print('Files Found with name {0} and Id  ({1})'.format(
                            item['name'], item['id']))
                page_token = response.get('nextPageToken', None)

                if page_token is None:
                    break

            except HttpError as err:
                if err.resp.status in [404]:
                    print(err)
                    return []
                else:
                    print(err)
                    return [{0}]
        return filelist

    def downloadFile(self, file_id, fileName):
        try:
            request = self.drive_service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100))

            downloadFilePath = f"{configdata['DownLoadFolder']}\\{fileName}"

            print(f"Saving File {downloadFilePath}")
            with io.open(downloadFilePath, 'wb') as f:
                fh.seek(0)
                f.write(fh.read())
            print(f"Saved File {downloadFilePath}")
            return True
        except Exception as ex:
            print(ex)
            return False

    def deleteFile(self, fileid, fileName):
        print(
            f"Deleting file from Drive with Id={fileid} and FileName={fileName}")
        try:
            response = self.drive_service.files().delete(fileId=fileid).execute()
            print(response)
            return True
        except Exception as ex:
            print(ex)
            return False
