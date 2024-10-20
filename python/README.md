# Reading Files
## Description
An application consisting of three parts: a REST API server written in Django using the Django REST Framework, a gRPC server, and a CLI application for working with them. The servers store files that can be accessed with get requests and receive either file metadata or the information stored in them.

## Stack technology
- Django
- DRF
- grpcio

## Installation
- `git clone https://github.com/TheSaintDeer/Reading-Files.git`

## Run 
Before running each part, it is recommended to create a virtual environment and download all libraries from the requirements.txt file.
- `python3 -m venv venv`
- `source env/bin/activate`
- `pip install -r requirements.txt`

### Run REST API
REST API server is located in the API directory
- `cd app/`
- `python manage.py migrate`
- `python manage.py runserver`

### Run gRPC
gRPC server is located in the gRPC directory
- `python grpc_server.py `

### Run CLI application
CLI application is located in the CLI directory
Usage:  python file-client.py [options] stat UUID
        python file-client.py read UUID
        python file-client.py

        Subcommands:
        stat                  Prints the file metadata in a human-readable manner.
        read                  Outputs the file content.

        Options:
        --help                Show this help message and exit.
        --backend=BACKEND     Set a backend to be used, choices are grpc and rest. Default is grpc.
        --grpc-server=NETLOC  Set a host and port of the gRPC server. Default is localhost:50051.
        --base-url=URL        Set a base URL for a REST server. Default is http://localhost/.
        --output=OUTPUT       Set the file where to store the output. Default is -, i.e. the stdout.

### Example commands
- `python file-client.py read 54514dcf-2004-4d54-8f6e-62e83cc14d65`
- `python file-client.py stat 54514dcf-2004-4d54-8f6e-62e83cc14d65 --backend rest --output a.txt`

### Example output
```json
{
    "name": "0514091c-8ea2-43f5-8c21-cddc722f703b.txt",
    "size": 5,
    "mimetype": "text/plain",
    "create_datetime": "2024-10-17T16:53:59.987253"
}
```
