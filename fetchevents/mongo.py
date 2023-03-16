import os
import json
import google.oauth2.credentials
from pymongo import MongoClient
from config import Config

# Set up MongoDB client and collection
client = MongoClient(Config.MONGO_URI)
db = client["functions_db"]
mongo_collection = db['users']


# Define MongoDB schema
user_schema = {
    'email': str,
    'credentials_data': dict,
    'credentials': str
}

class MongoDBError(Exception):
    pass

def db_add_user(email, credentials):
    credentials_data = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
        'expiry': credentials.expiry.isoformat(),
    }
    mongo_collection.update_one({'email': email}, {'$set': {'credentials_data': credentials_data, 'credentials': credentials.to_json()}}, upsert=True)


def db_get_user_credentials(email):
    try:
        user_doc = mongo_collection.find_one({'email': email})
        if user_doc and 'credentials' in user_doc:
            credentials_info = json.loads(user_doc['credentials'])
            credentials = google.oauth2.credentials.Credentials.from_authorized_user_info(credentials_info)
            return credentials

        else:
            raise MongoDBError(f"User not found in the database")
    except Exception as e:
        raise MongoDBError(f"Error getting user credentials from MongoDB: {e}")

