import json
import sqlite3
from Crypto.Hash import HMAC, SHA256
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


class SecureMessageAuthentication:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def calculate_sha256_hash(self, message):
        # Create a new SHA-256 hash object
        hash_object = SHA256.new(message)
        # Compute the SHA-256 hash of the provided data
        hashed_data = hash_object.digest()
        return hashed_data

    def generate_hmac(self, message):
        # Generate HMAC using the SHA-256 hash function and the secret key
        hmac = HMAC.new(self.secret_key, message, SHA256).digest()
        return hmac

    def authenticate_message(self, message):
        original_message = message
        sha256_hash = self.calculate_sha256_hash(message)
        hmac = self.generate_hmac(message)

        print("Original Message:", original_message.decode())
        print("SHA-256 Hash:", sha256_hash.hex())
        print("HMAC:", hmac.hex())
        return original_message.decode(), sha256_hash.hex(), hmac.hex()


class AES_encryption:
    def __init__(self, secret_key):
        self.secret_key = secret_key
    
    def AES_encrypt(self, message):
        # AES encryption using Cipher Block Chaining (CBC) mode
        cipher = AES.new(self.secret_key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(message, AES.block_size))
        return ciphertext, cipher

    def AES_decrypt(self, message):
        # AES decryption using the same key and initialization vector (iv) from the encryption
        ciphertext, cipher = self.AES_encrypt(message)
        decipher = AES.new(self.secret_key, AES.MODE_CBC, iv=cipher.iv)
        decrypted_data = unpad(decipher.decrypt(ciphertext), AES.block_size)
        return ciphertext, decrypted_data, cipher.iv

    def AES_encrypt_decrypt(self, message, decode=True):
        ciphertext, decrypted_data, iv = self.AES_decrypt(message)
        if decode:
            ciphertext = ciphertext.hex()
            decrypted_data = decrypted_data.decode()
        # Display the encrypted, and decrypted data
        print(f"Encrypted Message: {ciphertext}")
        print(f"Decrypted Message: {decrypted_data}")
        return ciphertext, iv.hex()


class RSA_encryption:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def RSA_encrypt(self, message):
        # Initialize an RSA cipher object with the PKCS1_OAEP padding scheme
        cipher = PKCS1_OAEP.new(self.secret_key)
        # RSA encryption using the public key
        encrypted_data = cipher.encrypt(message)
        return encrypted_data, cipher
    
    def RSA_decrypt(self, message):
        encrypted_data, cipher = self.RSA_encrypt(message)
        # RSA decryption using the private key
        decrypted_data = cipher.decrypt(encrypted_data)
        return encrypted_data, decrypted_data

    def RSA_encrypt_decrypt(self, message, decode=True):
        encrypted_data, decrypted_data = self.RSA_decrypt(message)
        if decode:
            decrypted_data = decrypted_data.decode()
        # Display the encrypted, and decrypted data
        print(f"\nEncrypted Message: {encrypted_data}")
        print(f"\nDecrypted Message: {decrypted_data}")


class DatabaseHandler:
    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name)
        self.create_table()

    def create_table(self):
        # Create a table if not exists
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS datas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_message TEXT,
                sha256_hash TEXT,
                hmac TEXT,
                encrypted_message TEXT,
                iv TEXT
            )
        ''')
        self.conn.commit()

    def insert_data(self, original_message, sha256_hash, hmac, encrypted_message, iv):
        # Insert data into the table
        self.conn.execute('''
            INSERT INTO datas (original_message, sha256_hash, hmac, encrypted_message, iv)
            VALUES (?, ?, ?, ?, ?)
        ''', (original_message, sha256_hash, hmac, encrypted_message, iv))
        self.conn.commit()


# exo_1
def exo_1():
    # Generate a Secret key for HMAC
    secret_key = get_random_bytes(16)
    
    # message to be authenticated
    user_input = bytes(input("\nEnter a message to authenticate: ").encode())
    
    authenticator = SecureMessageAuthentication(secret_key)
    authenticator.authenticate_message(user_input)

 
#exo_2
def exo_2():
    # Generate a random 128-bit key for AES encryption
    secret_key = get_random_bytes(16)
    
    # message to encrypt
    user_input = bytes(input("\nEnter a message to encrypt: ").encode())
    
    encryptor = AES_encryption(secret_key)
    encryptor.AES_encrypt_decrypt(user_input)


#exo_3
def exo_3():
    # Generate RSA key pair with a key length of 2048 bits
    pair_of_key = RSA.generate(2048)

    # mesage to encrypt
    user_input = bytes(input("\nEnter a message to encrypt: ").encode())
    
    authenticator = RSA_encryption(pair_of_key)
    authenticator.RSA_encrypt_decrypt(user_input)


#exo_4
def exo_4():
    while True:
        try:
            # Generate a random 128-bit key for AES encryption
            secret_key = get_random_bytes(16)

            # message to encrypt
            user_input = bytes(input("\nEnter a message to encrypt (Ctrl + C to exit): ").encode())
            
            encryptor = AES_encryption(secret_key)
            encrypted_message, iv = encryptor.AES_encrypt_decrypt(user_input)
            new_data = {"original_message": user_input.decode(), "encrypted_message": str(encrypted_message), "iv": str(iv)}
            # Écrire le fichier JSON mis à jour
            with open("conversation.json", "a") as file:
                file.write(json.dumps(new_data))
                file.write('\n')
        except KeyboardInterrupt:
            print("\nProgram terminated")
            break


#exo_5
def exo_5():
    db_handler = DatabaseHandler("secure_data.db")

    while True:
        try:
            # Generate a random 128-bit key for AES encryption
            secret_key = get_random_bytes(16)

            # Message to encrypt
            user_input = bytes(input("\nEnter a message to secure (Ctrl + C to exit): ").encode())
            
            # Authenticate message
            authenticator = SecureMessageAuthentication(secret_key)
            original_message, sha256_hash, hmac= authenticator.authenticate_message(user_input)

            # Encrypt message
            encryptor = AES_encryption(secret_key)
            encrypted_message, iv = encryptor.AES_encrypt_decrypt(user_input)

            # Insert data into the database
            db_handler.insert_data(
                original_message=original_message,
                sha256_hash=sha256_hash,
                hmac=hmac,
                encrypted_message=str(encrypted_message),
                iv=str(iv)
            )

        except KeyboardInterrupt:
            print("\nProgram terminated.")
            db_handler.conn.close()
            break


if __name__ == "__main__":
    exo_1()
    #exo_2()
    #exo_3()
    #exo_4()
    #exo_5()
