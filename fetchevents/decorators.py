import requests
from google.auth.exceptions import RefreshError
from datetime import datetime, time
from flask import (
    request,
    Request,
    redirect
)
from mongo import (db_add_user, db_get_user_credentials)


def validate_dates(function):
    def wrapper(request, *args, **kwargs):
        request_json = request.get_json()
        start_date_str = request_json['start_date']
        end_date_str = request_json['end_date']

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

            if start_date > end_date:
                raise ValueError("Start date should be before end date.")
            dates = (start_date, end_date)
        except (ValueError, TypeError):
            dates = None
        
        return function(dates=dates, *args, **kwargs)
    return wrapper

def fetchCredentials(function):
    def wrapper(*args, **kwargs):
        request_json = request.get_json()
        email = request_json['email']
        if(email == None):
            return "Please provide email"
        try: 
            credentials = db_get_user_credentials(email)
            if credentials == None or not credentials.valid:
                credentials = None
        except:
            # return redirect()
            return "There was a problem in fetching"

        # refresh_token = credentials.refresh_token
        # if not credentials.valid:

        #     # if credentials.expired and credentials.refresh_token:
        #     #     try:
        #     #         # Refresh the access token using the refresh token
        #     #         credentials.refresh("https://oauth2.googleapis.com/token")
        #     #         # Update the credentials in the database
        #     #         db_add_user(email, credentials)
            #     except RefreshError:
            #         # return redirect(url_for("login"))
            #         return "Unable to refresh credentials"
            # else:
            #     # return redirect(url_for("login"))
            #     return "Credentials have expired"

        return function(credentials=credentials, *args, **kwargs)
    return wrapper

