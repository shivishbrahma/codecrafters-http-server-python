import socket  # noqa: F401
import os
from argparse import ArgumentParser
from .pub_server import handle_request

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket, _ = server_socket.accept() # wait for client

    try:
        while True:
            req_buff = client_socket.recv(1024)
            if req_buff is None:
                break
            client_socket.sendall(handle_request(req_buff))

            break
    finally:
        client_socket.close()
        server_socket.close()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--directory", help="directory to serve", default=".")
    args = parser.parse_args()

    if args.directory:
        os.environ["BASE_DIR"] = args.directory

    main()
