import socket
import json

public_keys = {}

def handle_client(connection):
    global public_keys
    data = connection.recv(1024).decode()
    request = json.loads(data)

    if request['action'] == 'register':
        client_id = request['client_id']
        public_key = request['public_key']
        public_keys[client_id] = public_key
        response = {"status": "success", "message": "Public key registered"}
    elif request['action'] == 'get_key':
        client_id = request['client_id']
        if client_id in public_keys:
            response = {"status": "success", "public_key": public_keys[client_id]}
        else:
            response = {"status": "error", "message": "Client not found"}
    else:
        response = {"status": "error", "message": "Invalid action"}

    connection.send(json.dumps(response).encode())
    connection.close()

def start_pka():
    server_address = 'localhost'
    server_port = 4000
    socket_server = socket.socket()
    socket_server.bind((server_address, server_port))
    socket_server.listen(5)

    print(f"Public Key Authority is running on {server_address}:{server_port}")
    while True:
        connection, _ = socket_server.accept()
        handle_client(connection)

if __name__ == '__main__':
    start_pka()
