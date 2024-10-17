import argparse
import requests
import grpc
import service_file_pb2
import service_file_pb2_grpc
from google.protobuf.json_format import MessageToDict

# REST API
def rest_stat(uuid, base_url):
    try:
        url = f"{base_url}/file/{uuid}/stat/"
        response = requests.get(url)
        response.raise_for_status()
        print(f"{response.json()}")
    except requests.RequestException as e:
        print(f"REST request error: {e}")

def rest_read(uuid, base_url):
    try:
        url = f"{base_url}/file/{uuid}/read/"
        response = requests.get(url)
        response.raise_for_status()
        print(f"{response.content}")
    except requests.RequestException as e:
        print(f"REST request error: {e}")

# gRPC
def grpc_stat(uuid, grpc_server):
    channel = grpc.insecure_channel(grpc_server)
    stub = service_file_pb2_grpc.FileStub(channel)
    try:
        request = service_file_pb2.StatRequest(uuid=service_file_pb2.Uuid(value=uuid))
        response = stub.stat(request)
        metadata = MessageToDict(response.data)
        print(f"gRPC: File metadata for {uuid}: {metadata}")
    except grpc.RpcError as e:
        print(f"Error during gRPC request: {e}")

def grpc_read(uuid, grpc_server):
    channel = grpc.insecure_channel(grpc_server)
    stub = service_file_pb2_grpc.FileStub(channel)
    try:
        request = service_file_pb2.ReadRequest(uuid=service_file_pb2.Uuid(value=uuid))
        response = stub.read(request)
        print(f"gRPC: File content for {uuid}: {response.data.data}")
    except grpc.RpcError as e:
        print(f"Error during gRPC request: {e}")

def main():
    parser = argparse.ArgumentParser(description="CLI для работы с файлами через REST и gRPC.")
    
    # add commands
    parser.add_argument('command', choices=['stat', 'read'], help="Команда для выполнения: 'stat' для метаданных, 'read' для чтения файла.")
    parser.add_argument('uuid', help="UUID файла для запроса.")
    
    # add options
    parser.add_argument('--backend', choices=['grpc', 'rest'], default='grpc', help="Выбор backend сервера: grpc или rest.")
    parser.add_argument('--grpc-server', default='localhost:50051', help="Адрес gRPC сервера. По умолчанию localhost:50051.")
    parser.add_argument('--base-url', default='http://localhost', help="Базовый URL для REST сервера. По умолчанию http://localhost.")
    
    args = parser.parse_args()

    # choice of backend and command 
    if args.backend == 'grpc':
        if args.command == 'stat':
            grpc_stat(args.uuid, args.grpc_server)
        elif args.command == 'read':
            grpc_read(args.uuid, args.grpc_server)
    elif args.backend == 'rest':
        if args.command == 'stat':
            rest_stat(args.uuid, args.base_url)
        elif args.command == 'read':
            rest_read(args.uuid, args.base_url)

if __name__ == '__main__':
    main()
