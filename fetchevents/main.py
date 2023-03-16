import functions_framework

from flask import redirect

from decorators import (
    fetchCredentials,
    validate_dates
)

from google_utility.google_calendar_utility import get_calendar_events
from config import Config

@validate_dates
@fetchCredentials
def get_user_events(dates, credentials):
    if not dates:
        # handle the error by returning a custom error message
        return "Invalid date format. Please use YYYY-MM-DD format, and ensure that you are passing both dates."

    start_date, end_date = dates

    if credentials == None:
        return f"Coudn't find ur credentials visit: {Config.SIGNIN_FUNCTION_URL}"
    try:
        event_list = get_calendar_events(start_date, end_date, credentials)
        return (
            f"Your upcoming events are between "
            f"{start_date} and {end_date}: <br/> {', '.join(event_list)} <br/> "
        )
    except Exception as error:
        # handle the error by returning a custom error message
        return "Error fetching calendar events: {}".format(str(error))