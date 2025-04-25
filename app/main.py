import socket  # noqa: F401
import os
import threading
from argparse import ArgumentParser
from .pub_server import handle_request


def send_request(client_socket: socket.socket, addr):
    req_buff = client_socket.recv(1024)
    print(f"Received request from {addr}")
    print(req_buff.decode("utf-8"))
    if req_buff is None or len(req_buff) == 0:
        print("Client closed connection")
        client_socket.close()

    client_socket.send(handle_request(req_buff))
    client_socket.close()


def start_server(server_socket: socket.socket):
    client_socket = None
    while True:
        client_socket, addr = server_socket.accept()  # wait for client
        print(f"Connected to {addr}")
        threading.Thread(target=send_request, args=(client_socket, addr)).start()


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print(f"Server started on {server_socket.getsockname()}")
    try:
        start_server(server_socket)
    except KeyboardInterrupt:
        print("\nServer is shutting down...")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--directory", help="directory to serve", default=".")
    args = parser.parse_args()

    if args.directory:
        os.environ["BASE_DIR"] = args.directory

    main()
