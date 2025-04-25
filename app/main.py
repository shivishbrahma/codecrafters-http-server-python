import socket  # noqa: F401
import os
import threading
from argparse import ArgumentParser
from .pub_server import handle_request


def server_run(client_socket: socket.socket):
    while True:
        req_buff = client_socket.recv(1024)
        if req_buff is None:
            break
        client_socket.sendall(handle_request(req_buff))

        break


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print(f"Server started on {server_socket.getsockname()}")
    client_socket, addr = server_socket.accept()  # wait for client

    try:
        print(f"Connected to {addr}")
        threading.Thread(target=server_run, args=(client_socket,))
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
