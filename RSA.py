import random
import base64

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    d = 0
    x1, x2, x3 = 0, 1, phi
    y1, y2, y3 = 1, 0, e

    while y3 != 0:
        q = x3 // y3
        t1, t2, t3 = x1 - q * y1, x2 - q * y2, x3 - q * y3
        x1, x2, x3, y1, y2, y3 = y1, y2, y3, t1, t2, t3

    if x2 < 0:
        x2 += phi

    return x2

def generate_prime(bits):
    while True:
        num = random.getrandbits(bits)
        if num % 2 == 0:
            num += 1
        if is_prime(num):
            return num

def is_prime(n, k=5):  # Miller-Rabin primality test
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_rsa_keys(bits=1024):
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537  # Common choice for e
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    d = mod_inverse(e, phi)
    return (e, n), (d, n)  # Public key, Private key

# def encrypt_rsa(public_key, message):
#     e, n = public_key
#     encrypted_message = [pow(ord(char), e, n) for char in message]
#     return encrypted_message

def encrypt_rsa(public_key, plaintext):
    e, n = public_key
    encrypted_message = [pow(ord(char), e, n) for char in plaintext]
    # Encode hasil enkripsi ke Base64
    return base64.b64encode(str(encrypted_message).encode()).decode()

# def decrypt_rsa(private_key, encrypted_message):
#     d, n = private_key
#     decrypted_message = ''.join([chr(pow(char, d, n)) for char in encrypted_message])
#     return decrypted_message

def decrypt_rsa(private_key, encrypted_message):
    d, n = private_key
    # Decode dari Base64
    encrypted_message = eval(base64.b64decode(encrypted_message).decode())
    decrypted_message = ''.join([chr(pow(char, d, n)) for char in encrypted_message])
    return decrypted_message
