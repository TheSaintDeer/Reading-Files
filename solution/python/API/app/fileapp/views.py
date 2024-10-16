import os
import re
import mimetypes
import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse, Http404

FILES_DIR = './files'


class File:

    def get_filename(self, uuid):
        pattern = r"{uuid}\.*".format(uuid=uuid)

        for filename in os.listdir(FILES_DIR):
            if re.search(pattern, filename):
                return filename
            
    def get_mime_type(self, file_path):
        mime_type, encoding = mimetypes.guess_type(file_path)

        return mime_type
    
    def get_create_datetime(self, file_path):
        creation_time = os.path.getctime(file_path)
        creation_datetime = datetime.datetime.fromtimestamp(creation_time)
        iso_format = creation_datetime.isoformat()
    
        return iso_format
            

class FileStatView(APIView, File):
    
    def get(self, request, uuid):   

        filename = self.get_filename(uuid)
        print(filename)
        file_path = os.path.join(FILES_DIR, filename)
        if not os.path.exists(file_path):
            raise Http404("File not found")
        
        metadata = {
            "name": os.path.basename(file_path),
            "size": os.stat(file_path).st_size, # 1018 bytes
            "mimetype": self.get_mime_type(file_path), 
            "create_datetime": self.get_create_datetime(file_path)
        }

        return Response(metadata, status=status.HTTP_200_OK)


class FileReadView(APIView, File):
    
    def get(self, request, uuid):

        filename = self.get_filename(uuid)
        file_path = os.path.join(FILES_DIR, filename)
        if not os.path.exists(file_path):
            raise Http404("File not found")
        
        return FileResponse(
            open(file_path, 'rb'), 
            as_attachment=True, 
            filename=filename, 
            content_type=self.get_mime_type(file_path)
        )