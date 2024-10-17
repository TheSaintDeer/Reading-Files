import os
import re
import grpc
import mimetypes
import datetime
import service_file_pb2
import service_file_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp


FILES_DIR = './files'

class FileServicer(service_file_pb2_grpc.FileServicer):

    def stat(self, request, context):
        uuid = request.uuid.value
        pattern = r"{uuid}\.*".format(uuid=uuid)
        filename = ''
        for fn in os.listdir(FILES_DIR):
            if re.search(pattern, fn):
                filename = fn
                break

        file_path = f"{FILES_DIR}/{filename}"
        if not os.path.exists(file_path):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('File not found')
            return

        create_datetime = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
        timestamp = Timestamp()
        timestamp.FromDatetime(create_datetime)
        size = os.stat(file_path).st_size
        mimetype, encoding = mimetypes.guess_type(file_path)
        name = os.path.basename(file_path)
        
        return service_file_pb2.StatReply(
            data=service_file_pb2.StatReply.Data(
                create_datetime=timestamp,
                size=size,
                mimetype=mimetype,
                name=name
            )
        )

    def read(self, request, context):
        uuid = request.uuid.value
        pattern = r"{uuid}\.*".format(uuid=uuid)
        filename = ''
        for fn in os.listdir(FILES_DIR):
            if re.search(pattern, fn):
                filename = fn
                break

        file_path = f"{FILES_DIR}/{filename}"
        if not os.path.exists(file_path):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('File not found')
            return

        chunk_size = request.size if request.size > 0 else 1024
        try:
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    yield service_file_pb2.ReadReply(data=service_file_pb2.ReadReply.Data(data=chunk))
        except IOError as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'File read error: {str(e)}')
            return