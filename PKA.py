import socket
import json

keys = {}

def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    request_data = json.loads(request)

    if request_data["action"] == "register":
        keys[request_data["name"]] = request_data["public_key"]
        response = {"status": "registered"}
    elif request_data["action"] == "get_key":
        requested_name = request_data["name"]
        if requested_name in keys:
            response = {"public_key": keys[requested_name]}
        else:
            response = {"error": "Public key not found"}

    client_socket.send(json.dumps(response).encode())
    client_socket.close()

def start_pka():
    server_socket = socket.socket()
    server_socket.bind(("localhost", 4000))
    server_socket.listen(5)
    print("PKA is running on port 4000.")

    while True:
        client_socket, _ = server_socket.accept()
        handle_client(client_socket)

if __name__ == '__main__':
    start_pka()
