import pytz
from datetime import datetime, time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_calendar_events(start_date, end_date, credentials):
    try:
        service = build("calendar", "v3", credentials=credentials)
        start = datetime.combine(start_date, time.min).isoformat() + "Z"  # 'Z' indicates UTC time
        end = datetime.combine(end_date, time.max).isoformat() + "Z"  # 'Z' indicates UTC time

        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=start,
                timeMax=end,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        events = events_result.get("items", [])
        event_list = []

        if not events:
            event_list.append("No upcoming events found.")
        else:
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                event_time = (
                    datetime.fromisoformat(start)
                    .astimezone(pytz.timezone("Asia/Kolkata"))
                    .strftime("%Y-%m-%d %H:%M:%S")
                )
                event_list.append(f"{event_time} - {event['summary']}")

        return event_list
    except HttpError as error:
    # handle the error by returning a custom error message
        return ["Error fetching calendar events: {}".format(str(error))]
