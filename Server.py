# import socket
# import json
# from RSA import generate_keys, encrypt_rsa, decrypt_rsa
# from DES import des_encrypt, des_decrypt

# def request_public_key(name):
#     client_socket = socket.socket()
#     client_socket.connect(("localhost", 4000))
#     request = json.dumps({"action": "get_key", "name": name})
#     client_socket.send(request.encode())
#     response = json.loads(client_socket.recv(1024).decode())
#     client_socket.close()
#     return tuple(response.get("public_key"))

# def register_public_key(name, public_key):
#     client_socket = socket.socket()
#     client_socket.connect(("localhost", 4000))
#     registration_request = json.dumps({"action": "register", "name": name, "public_key": public_key})
#     client_socket.send(registration_request.encode())
#     client_socket.close()

# def start_server():
#     server_name = "Server"
#     public_key, private_key = generate_keys()

#     # Register public key with PKA
#     register_public_key(server_name, public_key)
#     print("Server's public key registered with PKA.")

#     # Get client's public key
#     client_public_key = request_public_key("Client")
#     if not client_public_key:
#         print("Failed to get client's public key.")
#         return
#     print("Client's public key received.")

#     # Start server socket
#     server_socket = socket.socket()
#     server_socket.bind(("localhost", 3000))
#     server_socket.listen(1)
#     print("Server is running and waiting for connection.")

#     conn, addr = server_socket.accept()
#     print(f"Connection established with {addr}")

#     while True:
#         # Receive client's message
#         client_data = conn.recv(1024).decode()
#         client_data = json.loads(client_data)

#         if "end" in client_data and client_data["end"]:
#             print("Client has ended the communication.")
#             break

#         rsa_decrypted = decrypt_rsa(client_data, private_key)
#         des_decrypted = des_decrypt(rsa_decrypted, "D4AF3BA2C945ED58")
#         print(f"Client: {des_decrypted}")

#         # Server sends response
#         server_message = input("Server: Enter response (or 'end' to exit): ")
#         if server_message.lower() == 'end':
#             conn.send(json.dumps({"end": True}).encode())
#             print("Ending communication.")
#             break

#         # Encrypt with DES, then with RSA
#         des_encrypted = des_encrypt(server_message, "D4AF3BA2C945ED58")
#         rsa_encrypted = encrypt_rsa(des_encrypted, client_public_key)
#         conn.send(json.dumps(rsa_encrypted).encode())

#     conn.close()

# if __name__ == '__main__':
#     start_server()

import DES as des
import socket

def start_server():
    server_address = 'localhost'
    server_port = 3000
    encryption_key = 'D4AF3BA2C945ED58'

    socket_server = socket.socket()
    socket_server.bind((server_address, server_port))

    print(f"Server is running at {server_address}:{server_port}")

    socket_server.listen(1)
    connection, client_address = socket_server.accept()
    print(f"Accepted connection from: {client_address}")

    while True:
        # Terima data dari client
        received_data = connection.recv(1024).decode()
        
        if not received_data:  # Jika tidak ada data, keluar dari loop
            print("No data received, closing connection.")
            break

        # Jika client mengirim 'end', server akan menutup koneksi
        if received_data.lower().strip() == 'end':
            print("Received 'end' message. Closing connection.")
            break

        # Tampilkan pesan terenkripsi yang diterima
        print(f"Encrypted message received from client: {received_data}")

        # Dekripsi pesan yang diterima
        decrypted_message = des.des_decrypt(received_data, encryption_key)
        print(f"Decrypted message: {decrypted_message}")

    connection.close()

if __name__ == '__main__':
    start_server()
