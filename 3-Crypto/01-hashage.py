
"""
Ce code montre l'utilisation du hachage SHA-256 .
La fonction de hachage SHA-256 est une fonction de hachage cryptographique unidirectionnelle.
Cela signifie qu'une fois les données hachées à l'aide de SHA-256, elles ne peuvent pas être inversées ou déchiffrées.
obtenir les données originales. Le processus est conçu pour être irréversible pour des raisons de sécurité.
"""

from Crypto.Hash import SHA256

# Data to be hashed
data = b"ID296595 EPMI!"

# Create a new SHA-256 hash object
hash_object = SHA256.new(data)

# Compute the SHA-256 hash of the provided data
hashed_data = hash_object.digest()

# Display the original data and the resulting SHA-256 hash
print(f"Original Data: {data}")
print(f"SHA-256 Hash in Bytes: {hashed_data}")
print(f"SHA-256 Hash: {hash_object.hexdigest()}")
