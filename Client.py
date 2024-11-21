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

# def start_client():
#     client_name = "Client"
#     public_key, private_key = generate_keys()

#     # Register public key with PKA
#     register_public_key(client_name, public_key)
#     print("Client's public key registered with PKA.")

#     # Get server's public key
#     server_public_key = request_public_key("Server")
#     if not server_public_key:
#         print("Failed to get server's public key.")
#         return
#     print("Server's public key received.")

#     # Connect to server
#     server_socket = socket.socket()
#     server_socket.connect(("localhost", 3000))
#     print("Connected to server.")

#     while True:
#         # Client sends message
#         client_message = input("Client: Enter plain text (or 'end' to exit): ")
#         if client_message.lower() == 'end':
#             server_socket.send(json.dumps({"end": True}).encode())
#             print("Ending communication.")
#             break

#         # Encrypt with DES, then with RSA
#         des_encrypted = des_encrypt(client_message, "D4AF3BA2C945ED58")
#         rsa_encrypted = encrypt_rsa(des_encrypted, server_public_key)
#         server_socket.send(json.dumps(rsa_encrypted).encode())

#         # Wait for server's response
#         server_response = server_socket.recv(1024).decode()
#         server_data = json.loads(server_response)

#         if "end" in server_data and server_data["end"]:
#             print("Server has ended the communication.")
#             break

#         rsa_decrypted = decrypt_rsa(server_data, private_key)
#         des_decrypted = des_decrypt(rsa_decrypted, "D4AF3BA2C945ED58")
#         print(f"Server: {des_decrypted}")

#     server_socket.close()

# if __name__ == '__main__':
#     start_client()

import DES as des
import socket

def start_client():
    server_address = 'localhost'
    server_port = 3000
    encryption_key = 'D4AF3BA2C945ED58'

    socket_client = socket.socket()
    socket_client.connect((server_address, server_port))

    while True:
        # Mengambil pesan dari user untuk dikirimkan
        message = input("Enter message to send (type 'end' to stop): ")

        # Jika pesan 'end', client akan mengirim pesan 'end' dan menutup koneksi
        if message.lower().strip() == 'end':
            socket_client.send(message.encode())
            print("Sent 'end' message. Closing connection.")
            break
        
        # Enkripsi pesan menggunakan DES
        encrypted_message = des.des_encrypt(message, encryption_key)

        # Kirim pesan terenkripsi ke server
        socket_client.send(encrypted_message.encode())
        print(f"Sent encrypted message: {encrypted_message}")

    socket_client.close()

if __name__ == '__main__':
    start_client()
