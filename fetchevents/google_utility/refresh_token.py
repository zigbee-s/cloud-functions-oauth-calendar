from google.oauth2.credentials import Credentials
import requests
from datetime import datetime, timedelta
from config import Config

def refresh_token(credentials):
    GOOGLE_CLIENT_ID = Config.GOOGLE_CLIENT_ID
    GOOGLE_CLIENT_SECRET = Config.GOOGLE_CLIENT_SECRET

    SCOPES=["https://www.googleapis.com/auth/userinfo.profile", 
                "https://www.googleapis.com/auth/userinfo.email", 
                "openid", 
                "https://www.googleapis.com/auth/calendar"]

    params = {
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "refresh_token": credentials.refresh_token,
        "grant_type": "refresh_token"
    }

    try:
        response = requests.post("https://oauth2.googleapis.com/token", data=params)
        response.raise_for_status()
        # Calculate the new expiry date based on the current time and the expires_in value in the response
        new_expiry = datetime.now() + timedelta(seconds=response.json()['expires_in'])

        # Create the new Credentials object with the updated access token and expiry date
        new_credentials = Credentials(
            token=response.json()['access_token'],
            refresh_token=credentials.refresh_token,
            token_uri=credentials.token_uri,
            client_id=GOOGLE_CLIENT_ID,
            client_secret=GOOGLE_CLIENT_SECRET,
            scopes=SCOPES,
            expiry=new_expiry
        )

        return new_credentials
    except requests.exceptions.HTTPError as error:
        # Handle HTTP errors
        raise Exception(f"HTTP error occurred: {error}")
    
    except Exception as error:
        raise Exception(f"Error occured: {error}")