import time
import grpc
import service_file_pb2_grpc
from concurrent import futures

from FileServicer import FileServicer


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_file_pb2_grpc.add_FileServicer_to_server(FileServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(60*60)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    main()
