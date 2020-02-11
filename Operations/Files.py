from __future__ import print_function


class FilesOperation:
    def __init__(self, drive_service, http):
        self.drive_service = drive_service
        self.imageMimeType = 'image/jpeg'


def callback(request_id, response, exception):
    if exception:
        print("Exception:", exception)


def uploadFile(self, files):
    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath, mimetype=mimetype)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))


def listFiles(self,folderId=None,parentid=None):
    query=f""
    results = drive_service.files().list(
        pageSize=size, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))

def downloadFile(self, file_id):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with io.open(filepath, 'wb') as f:
        fh.seek(0)
        f.write(fh.read())


def deleteFile(self, files):
    while(len(files) > 0):
        batch = self.drive_service.new_batch_http_request(callback=callback)
        batchSize = min(len(files), 99)
        for i in range(batchSize):
            print("Deleting", files[0])
            batch.add(service.files().delete(
                fileId=files[0]
            ))
            del files[0]

        batch.execute(http=http)
