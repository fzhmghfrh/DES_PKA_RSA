import RSA as rsa
import DES as des
import socket
import json

def receive_full_data(connection):
    buffer_size = 4096  # Ukuran buffer lebih besar
    data = b""  # Data diterima dalam bentuk byte
    while True:
        part = connection.recv(buffer_size)  # Terima data dalam potongan
        data += part
        if len(part) < buffer_size:  # Jika data yang diterima kurang dari buffer_size, berarti selesai
            break
    return data.decode()  # Decode data menjadi string

def start_server():
    # Generate RSA keys
    private_key, public_key = rsa.generate_rsa_keys()
    server_id = "server"

    # Register public key with PKA
    pka_socket = socket.socket()
    pka_socket.connect(('localhost', 4000))
    register_request = {
        "action": "register",
        "client_id": server_id,
        "public_key": public_key
    }
    pka_socket.send(json.dumps(register_request).encode())
    pka_socket.close()

    # Start server
    server_address = 'localhost'
    server_port = 3000
    socket_server = socket.socket()
    socket_server.bind((server_address, server_port))
    socket_server.listen(1)

    print(f"Server is running on {server_address}:{server_port}")
    connection, _ = socket_server.accept()

    # Receive encrypted DES key
    # encrypted_key_data = json.loads(connection.recv(4096).decode())
    encrypted_key_data = json.loads(receive_full_data(connection))
    encrypted_des_key = encrypted_key_data['key']
    des_key = rsa.decrypt_rsa(private_key, encrypted_des_key)

    while True:
        encrypted_message = connection.recv(4096).decode()
        if not encrypted_message:
            break

        decrypted_message = des.des_decrypt(encrypted_message, des_key)
        print(f"Decrypted message from client: {decrypted_message}")

        if decrypted_message.lower().strip() == 'end':
            break

        reply_message = input("Enter reply: ")
        encrypted_reply = des.des_encrypt(reply_message, des_key)
        connection.send(encrypted_reply.encode())

    connection.close()

if __name__ == '__main__':
    start_server()
