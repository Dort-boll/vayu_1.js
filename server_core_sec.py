import os
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import hashlib
import hmac

class SecureMessagingApp:
    def __init__(self):
        self.user_data = {}  # Store user data (e.g., passwords, keys)
        self.messages = {}   # Store encrypted messages

    def register_user(self, username, password):
        # Store hashed password securely (e.g., in Keychain)
        salt = os.urandom(16)
        key = self.derive_key(password, salt)
        self.user_data[username] = {'salt': salt, 'key': key}

    def authenticate_user(self, username, password):
        if username not in self.user_data:
            return False
        stored_salt = self.user_data[username]['salt']
        stored_key = self.user_data[username]['key']
        derived_key = self.derive_key(password, stored_salt)
        return derived_key == stored_key

    def derive_key(self, password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def send_message(self, sender, recipient, message):
        if sender not in self.user_data or recipient not in self.user_data:
            raise ValueError("Invalid sender or recipient")
        if not self.messages.get(recipient):
            self.messages[recipient] = []
        key = self.user_data[recipient]['key']
        encrypted_message = self.encrypt_message(message, key)
        self.messages[recipient].append((sender, encrypted_message))

    def receive_messages(self, recipient):
        if recipient not in self.user_data:
            raise ValueError("Invalid recipient")
        if not self.messages.get(recipient):
            return []
        key = self.user_data[recipient]['key']
        decrypted_messages = []
        for sender, encrypted_message in self.messages[recipient]:
            decrypted_message = self.decrypt_message(encrypted_message, key)
            decrypted_messages.append((sender, decrypted_message))
        return decrypted_messages

    def encrypt_message(self, message, key):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ct = encryptor.update(message.encode()) + encryptor.finalize()
        return iv + ct

    def decrypt_message(self, encrypted_message, key):
        iv = encrypted_message[:16]
        ct = encrypted_message[16:]
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        return decryptor.update(ct) + decryptor.finalize()

    def hmac_signature(self, message, key):
        h = hmac.new(key, message, hashlib.sha256)
        return h.digest()

    def verify_hmac(self, message, signature, key):
        return hmac.compare_digest(self.hmac_signature(message, key), signature)

# Usage example
app = SecureMessagingApp()
app.register_user('alice', 'password123')
app.register_user('bob', 'securepassword')
app.send_message('alice', 'bob', 'Hello, Bob!')
messages = app.receive_messages('bob')
for sender, message in messages:
    print(f"Message from {sender}: {message}")
