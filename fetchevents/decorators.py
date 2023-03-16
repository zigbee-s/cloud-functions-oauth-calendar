from google.auth.exceptions import RefreshError
from datetime import datetime, time
from flask import (
    request, redirect
)
from mongo import (db_add_user, db_get_user_credentials)
from google_utility.refresh_token import refresh_token
from config import Config

def validate_dates(function):
    def wrapper(request, *args, **kwargs):
        try:
            request_json = request.get_json()
            start_date_str = request_json['start_date']
            end_date_str = request_json['end_date']
        except:
            raise Exception("Enter both dates")

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

            if start_date > end_date:
                raise ValueError("Start date should be before end date.")
            dates = (start_date, end_date)
        except ValueError as ve:
            return f"ValueError: {str(ve)}"
        except TypeError as te:
            return f"TypeError: {str(te)}"
        except Exception as e:
            return f"Exception occurred: {str(e)}"

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
            if not credentials.valid:
                try:
                    credentials = refresh_token(credentials)
                    db_add_user(email, credentials)
                except RefreshError:
                    print(f"Error occured: {error}")
                    return redirect(Config.SIGNIN_FUNCTION_URL)
                
        except Exception as error:
            print(f"Error occured: {error}")
            return redirect(Config.SIGNIN_FUNCTION_URL)
        return function(credentials=credentials, *args, **kwargs)
    return wrapper