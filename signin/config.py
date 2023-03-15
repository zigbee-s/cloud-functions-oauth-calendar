import os
import secrets

class Config:
    SIGNIN_FUNCTION_URL = 'https://us-central1-task-380216.cloudfunctions.net/signin'
    CALENDAR_FUNCTION_URL = "https://us-central1-task-380216.cloudfunctions.net/calendar"
    MONGO_URI = 'mongodb+srv://gauraang:shadow%401231@cluster0.i7bb8j8.mongodb.net/?retryWrites=true&w=majority'
    CLIENT_ID = "143131797716-n54c0mhqgvbjo4ivj81ok5j8afl3r4hf.apps.googleusercontent.com"
    CLIENT_SECRET = "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"