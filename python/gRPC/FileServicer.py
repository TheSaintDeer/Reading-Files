import os
import grpc
import service_file_pb2
import service_file_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp



class FileServicer(service_file_pb2_grpc.FileServicer):

    def stat(self, request, context):
        uuid = request.uuid.value
        file_path = f"./files/{uuid}"

        if not os.path.exists(file_path):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('File not found')
            return service_file_pb2.StatReply()

        stat_info = os.stat(file_path)
        create_datetime = Timestamp()
        create_datetime.FromSeconds(stat_info.st_ctime)

        metadata = service_file_pb2.StatReply.Data(
            create_datetime=create_datetime,
            size=stat_info.st_size,
            mimetype='text/plain',
            name=os.path.basename(file_path)
        )

        return service_file_pb2.StatReply(data=metadata)

    def read(self, request, context):
        uuid = request.uuid.value
        file_path = f"./files/{uuid}"

        if not os.path.exists(file_path):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('File not found')
            return service_file_pb2.ReadReply()

        chunk_size = request.size if request.size > 0 else 1024
        try:
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    yield service_file_pb2.ReadReply(data=service_file_pb2.ReadReply.Data(data=chunk))
        except IOError as e:
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details(f'File read error: {e}')