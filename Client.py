import RSA as rsa
import DES as des
import socket
import json

def start_client():
    # Generate RSA keys
    private_key, public_key = rsa.generate_rsa_keys()
    client_id = "client1"

    # Register public key with PKA
    pka_socket = socket.socket()
    pka_socket.connect(('localhost', 4000))
    register_request = {
        "action": "register",
        "client_id": client_id,
        "public_key": public_key
    }
    pka_socket.send(json.dumps(register_request).encode())
    pka_socket.close()

    # Retrieve server's public key
    pka_socket = socket.socket()
    pka_socket.connect(('localhost', 4000))
    get_key_request = {"action": "get_key", "client_id": "server"}
    pka_socket.send(json.dumps(get_key_request).encode())
    response = json.loads(pka_socket.recv(1024).decode())
    pka_socket.close()

    server_public_key = response['public_key']

    # Generate DES key and encrypt it with server's public key
    des_key = des.generate_key()
    encrypted_des_key = rsa.encrypt_rsa(server_public_key, des_key)

    # Send encrypted DES key to server
    server_socket = socket.socket()
    server_socket.connect(('localhost', 3000))
    server_socket.send(json.dumps({"key": encrypted_des_key}).encode())
    
    while True:
        message = input("Enter plain text (type 'end' to terminate): ")
        encrypted_message = des.des_encrypt(message, des_key)
        server_socket.send(encrypted_message.encode())

        if message.lower().strip() == 'end':
            break

        response = server_socket.recv(1024).decode()
        print(f"Encrypted response: {response}")
        print(f"Decrypted response: {des.des_decrypt(response, des_key)}")

    server_socket.close()

if __name__ == '__main__':
    start_client()
