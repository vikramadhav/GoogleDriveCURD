from __future__ import print_function
import os
import shutil
import io
import json
from googleapiclient.errors  import HttpError
from googleapiclient.http  import MediaFileUpload
from googleapiclient.http  import MediaIoBaseDownload


# Open the JSOn configuration file and Fetch Data
with open(os.path.join(os.getcwd(),'config.json')) as config_file:
    data = json.load(config_file)


class FilesOperation:
    def __init__(self, drive_service):
        self.drive_service = drive_service
        self.imageMimeType = 'image/jpeg'
        self.UnknownMimeType = 'application/vnd.google-apps.unknown'
        

    def callback(self, request_id, response, exception):
        if exception:
            print("Exception:", exception)

    def uploadFile(self, filePath, parentid):
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
        if not fileId and not fileName and not parentid:
            print("No Valid Parameter are found. Aborting!")
        if parentid:
            query += f"parents in '{parentid}' and "

        if fileName:
            query += f"name='{fileName}' "
        elif fileId:
            query += f"id='{fileId}' '"

        query += " and mimeType != 'application/vnd.google-apps.folder' and trashed=false"
        try:
            results = self.drive_service.files().list(q=query, spaces='drive',

                                                      pageSize=size, fields="nextPageToken,files(id, name)").execute()

            items = results.get('files', [])
            if not items:
                print('No Duplication found.')
                return []
            else:
                print('Files:')
                for item in items:
                    print('Duplicate File Found with name {0} and Id  ({1})'.format(
                        item['name'], item['id']))

            return items
        except HttpError as err:
            if err.resp.status in [404]:
                print(err)
                return []
            else:
                print(err)
                return [{0}]

    def downloadFile(self, file_id, fileName):
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

        downloadFilePath = f"{data['DownLoadFolder']}\\{fileName}"

        print(f"Saving File {downloadFilePath}")
        with io.open(downloadFilePath, 'wb') as f:
            fh.seek(0)
            f.write(fh.read())
        print(f"Saved File {downloadFilePath}")

    # def deleteFile(self, files):
    #     while(len(files) > 0):
    #         batch = self.drive_service.new_batch_http_request(
    #             callback=self.callback)
    #         batchSize = min(len(files), 99)
    #         for i in range(batchSize):
    #             print("Deleting", files[0])
    #             batch.add(self.service.files().delete(
    #                 fileId=files[0]
    #             ))
    #             del files[0]

    #         batch.execute(http=self.http)
