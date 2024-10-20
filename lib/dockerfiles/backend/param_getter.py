import json
import boto3
from botocore.exceptions import ClientError

def get_secret(secret_name):
    """Retrieve a secret from AWS Secrets Manager."""
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name='us-east-1'  # e.g., 'us-west-2'
    )

    try:
        # Retrieve the secret
        response = client.get_secret_value(SecretId=secret_name)
       
        # Parse the secret string (assuming JSON format)
        secret = json.loads(response['SecretString'])
        return secret['MONGO_USER'], secret['MONGO_PASS']
   
    except ClientError as e:
        print(f"Error retrieving secret: {e}")
        return None, None