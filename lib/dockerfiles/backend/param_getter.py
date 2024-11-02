import json
import boto3
from cryptography.fernet import Fernet
from botocore.exceptions import ClientError
import os



def get_secret(secret_name):
    """Retrieve a secret from AWS Secrets Manager."""
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name='us-east-1')

    try:
        # Retrieve the secret
        response = client.get_secret_value(SecretId=secret_name)

        # Parse the secret string (assuming JSON format)
        secret = json.loads(response['SecretString'])
        return secret['MONGO_USER'], secret['MONGO_PASS']
   
    except ClientError as e:
        print(f"Error retrieving secret from AWS KMS: {e}")
        encryption_key = os.getenv("ZAMIKX_ENCRYPTION_KEY")
        if encryption_key is None:
            raise ValueError("ENCRYPTION_KEY environment variable not set.")
        # Step 1: Load the key (retrieved securely from an environment variable, AWS Secrets Manager, etc.)
        # key = b'your-generated-encryption-key'  # This should be securely retrieved

        # Step 2: Use the key to create a cipher object
        cipher = Fernet(encryption_key)

        # Step 3: Read the encrypted file
        with open('backend/config.enc', 'rb') as enc_file:
            encrypted_data = enc_file.read()

        # Step 4: Decrypt the file
        decrypted_data = cipher.decrypt(encrypted_data)

        # Step 5: Parse the decrypted data as JSON (if your config was JSON formatted)
        config = json.loads(decrypted_data)

        # Step 6: Access the sensitive data in your code
        username = config['username']
        password = config['password']
        return username , password

