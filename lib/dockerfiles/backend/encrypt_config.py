from cryptography.fernet import Fernet

# Step 1: Generate a key (do this once and store the key securely, not in code)
key = Fernet.generate_key()
print(f"Encryption Key: {key.decode()}")  # Store this securely, e.g., in AWS Secrets Manager

# Step 2: Use the key to create a cipher object
cipher = Fernet(key)

# Step 3: Read the plaintext config file
with open('./config.json', 'rb') as file:
    config_data = file.read()

# Step 4: Encrypt the config file
encrypted_data = cipher.encrypt(config_data)

# Step 5: Save the encrypted data to a file
with open('config.enc', 'wb') as enc_file:
    enc_file.write(encrypted_data)

print("Config file encrypted and saved as config.enc")
