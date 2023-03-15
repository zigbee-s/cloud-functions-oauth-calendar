import os
import logging
from typing import Dict
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from flask import redirect, render_template
from mongo import db_add_user
import requests
from config import Config

logging.basicConfig(level=logging.INFO)

def getFlow():
    #os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    redirect_uri = Config.SIGNIN_FUNCTION_URL

    scopes = ["https://www.googleapis.com/auth/userinfo.profile",
              "https://www.googleapis.com/auth/userinfo.email",
              "openid",
              "https://www.googleapis.com/auth/calendar"]
    client_config = {
        'web': {
            'client_id': Config.CLIENT_ID,
            'client_secret': Config.CLIENT_SECRET,
            'redirect_uris': [redirect_uri],
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
        }
    }

    return Flow.from_client_config(client_config=client_config, scopes=scopes,
                                   redirect_uri=redirect_uri)
    

def getUserInfo(credentials):
    user_info = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?scope=email',
                             headers={'Authorization': f'Bearer {credentials.token}'})
    user_info = user_info.json()
    return user_info['id'], user_info['email']

def google_oauth(request):
    flow = getFlow()
    try:
        authorization_url, _ = flow.authorization_url(access_type='offline', prompt='consent')
        if 'code' not in request.args:
            return redirect(authorization_url)
        else:
            flow.fetch_token(code=request.args['code'])
            credentials = flow.credentials
            
            user_id, email = getUserInfo(credentials)

            db_add_user(email=email, credentials=credentials)
            logging.info(f"New user added with the email: {email}")
            # Return Visit Calendar button
            visit_calendar_url = Config.CALENDAR_FUNCTION_URL
            return render_template('authenticated.html', url=visit_calendar_url)
    except Exception as e:
        logging.error(str(e))
        return 'Error: {}'.format(str(e))
