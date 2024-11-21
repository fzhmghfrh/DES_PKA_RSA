import socket
import json
from RSA import generate_keys, encrypt_rsa, decrypt_rsa
from DES import des_encrypt, des_decrypt

def request_public_key(name):
    client_socket = socket.socket()
    client_socket.connect(("localhost", 4000))
    request = json.dumps({"action": "get_key", "name": name})
    client_socket.send(request.encode())
    response = json.loads(client_socket.recv(1024).decode())
    client_socket.close()
    return tuple(response.get("public_key"))

def register_public_key(name, public_key):
    client_socket = socket.socket()
    client_socket.connect(("localhost", 4000))
    registration_request = json.dumps({"action": "register", "name": name, "public_key": public_key})
    client_socket.send(registration_request.encode())
    client_socket.close()

def start_server():
    server_name = "Server"
    public_key, private_key = generate_keys()

    # Register public key with PKA
    register_public_key(server_name, public_key)
    print("Server's public key registered with PKA.")

    # Get client's public key
    client_public_key = request_public_key("Client")
    if not client_public_key:
        print("Failed to get client's public key.")
        return
    print("Client's public key received.")

    # Start server socket
    server_socket = socket.socket()
    server_socket.bind(("localhost", 3000))
    server_socket.listen(1)
    print("Server is running and waiting for connection.")

    conn, addr = server_socket.accept()
    print(f"Connection established with {addr}")

    while True:
        # Receive client's message
        client_data = conn.recv(1024).decode()
        if not client_data:
            continue
        client_data = json.loads(client_data)

        if "end" in client_data and client_data["end"]:
            print("Client has ended the communication.")
            break

        # Decrypt using RSA and then DES
        rsa_decrypted = decrypt_rsa(client_data, private_key)
        des_decrypted = des_decrypt(rsa_decrypted, "D4AF3BA2C945ED58")
        print(f"Client: {des_decrypted}")

    conn.close()

if __name__ == '__main__':
    start_server()
