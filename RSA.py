import random

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def generate_keys():
    # Generate two large primes (for simplicity, use small primes)
    primes = [101, 103, 107, 109, 113]
    p = random.choice(primes)
    q = random.choice(primes)
    while p == q:
        q = random.choice(primes)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randint(2, phi - 1)
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    d = mod_inverse(e, phi)
    return (e, n), (d, n)

def encrypt_rsa(message, public_key):
    e, n = public_key
    return [pow(ord(char), e, n) for char in message]

def decrypt_rsa(ciphertext, private_key):
    d, n = private_key
    return ''.join([chr(pow(char, d, n)) for char in ciphertext])
