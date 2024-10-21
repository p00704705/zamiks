from pymongo import MongoClient
from urllib.parse import quote_plus
from .param_getter import get_secret



def connect_to_mongo():
    """Connect to the MongoDB Atlas database using credentials from AWS Secrets Manager."""
    # Fetch MongoDB Atlas credentials
    username, password = get_secret("mongo/atlas_credentials")
   
    if username is None or password is None:
        raise Exception("Failed to retrieve MongoDB credentials.")

    # URL encode the username and password
    username = quote_plus(username)
    password = quote_plus(password)

    # Create the MongoDB connection string
    connection_string = f"mongodb+srv://{username}:{password}@zamikx-db-cluster.joklu.mongodb.net/?retryWrites=true&w=majority&appName=zamikx-db-cluster"
   
    # Create a MongoDB client
    client = MongoClient(connection_string)
    db_name = "zamikx-db"

    # Access the database
    db = client[db_name]
   
    # Access the collection (it will be created if it doesn't exist)
    collection = db["summaries"]
   
    return collection

def store_text(original_text, summarized_text):
    """Store original and summarized text in MongoDB."""
    collection = connect_to_mongo()
   
    # Create a document to insert
    document = {
        "original_text": original_text,
        "summarized_text": summarized_text
    }
   
    # Insert the document into the collection
    result = collection.insert_one(document)
   
    # Print the ID of the inserted document
    print(f"Inserted document with ID: {result.inserted_id}")
