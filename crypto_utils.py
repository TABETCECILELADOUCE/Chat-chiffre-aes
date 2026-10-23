import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

# Clé de chiffrement AES-256 (32 octets)
# Dans un projet réel, cette clé est transmise de manière sécurisée ou dérivée via DH.
SECRET_KEY = b'12345678901234567890123456789012'

def encrypt_message(plain_text: str) -> str:
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plain_text.encode('utf-8')) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_data) + encryptor.finalize()
    
    # On concatène IV + Texte Chiffré et on encode en Base64
    return base64.b64encode(iv + ct).decode('utf-8')

def decrypt_message(cipher_text_b64: str) -> str:
    data = base64.b64decode(cipher_text_b64.encode('utf-8'))
    iv = data[:16]
    ct = data[16:]
    
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ct) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    plain_text = unpadder.update(padded_data) + unpadder.finalize()
    return plain_text.decode('utf-8')