import argparse
import requests
import grpc
import service_file_pb2
import service_file_pb2_grpc
import sys
import json
from google.protobuf.json_format import MessageToDict

# REST API
def rest_stat(uuid, base_url, output):
    try:
        url = f"{base_url}:8000/file/{uuid}/stat/"
        response = requests.get(url)
        response.raise_for_status()
        output_metadata(response.json(), output)
    except requests.RequestException as e:
        print(f"REST request error: {e}")

def rest_read(uuid, base_url, output):
    try:
        url = f"{base_url}:8000/file/{uuid}/read/"
        response = requests.get(url)
        response.raise_for_status()
        output_file(response.content, output)
    except requests.RequestException as e:
        print(f"REST request error: {e}")

# gRPC
def grpc_stat(uuid, grpc_server, output):
    channel = grpc.insecure_channel(grpc_server)
    stub = service_file_pb2_grpc.FileStub(channel)
    try:
        request = service_file_pb2.StatRequest(uuid=service_file_pb2.Uuid(value=uuid))
        response = stub.stat(request)
        output_metadata(MessageToDict(response.data), output)
    except grpc.RpcError as e:
        print(f"gRPC request error: {e}")

def grpc_read(uuid, grpc_server, output):
    channel = grpc.insecure_channel(grpc_server)
    stub = service_file_pb2_grpc.FileStub(channel)
    try:
        request = service_file_pb2.ReadRequest(uuid=service_file_pb2.Uuid(value=uuid))
        for response in stub.read(request):
            output_file(response.data.data, output)
    except grpc.RpcError as e:
        print(f"gRPC request error: {e}")

# writing
def output_metadata(metadata, output):
    if output == "-":
        print(f"{metadata}")
    else:
        with open(output, "w") as f:
            f.write(json.dumps(metadata))

def output_file(file_content, output):
    if output == "-":
        sys.stdout.buffer.write(file_content)
    else:
        with open(output, "wb") as f:
            f.write(file_content)


def main():
    parser = argparse.ArgumentParser(description="CLI application which retrieves and prints data.")
    
    # add commands
    parser.add_argument('command', choices=['stat', 'read'], help="Commands: 'stat' for metadata, 'read' for reading file.")
    parser.add_argument('uuid', help="File UUID.")
    
    # add options
    parser.add_argument('--backend', choices=['grpc', 'rest'], default='grpc', help="Set a backend to be used, choices are grpc and rest. Default is grpc.")
    parser.add_argument('--grpc-server', default='localhost:50051', help="Set a host and port of the gRPC server. Default is localhost:50051.")
    parser.add_argument('--base-url', default='http://localhost', help="Set a base URL for a REST server. Default is http://localhost/.")
    parser.add_argument('--output', default='-', help="Set the file where to store the output. Default is -, i.e. the stdout.")
    
    args = parser.parse_args()

    # choice of backend and command 
    if args.backend == 'grpc':
        if args.command == 'stat':
            grpc_stat(args.uuid, args.grpc_server, args.output)
        elif args.command == 'read':
            grpc_read(args.uuid, args.grpc_server, args.output)
    elif args.backend == 'rest':
        if args.command == 'stat':
            rest_stat(args.uuid, args.base_url, args.output)
        elif args.command == 'read':
            rest_read(args.uuid, args.base_url, args.output)

if __name__ == '__main__':
    main()
