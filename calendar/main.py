import json
import urllib.request
from config import Config

def calendar(request):
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        email = request.form['email']
        data = {'start_date': start_date, 'end_date': end_date, 'email': email}
        headers = {'Content-type': 'application/json'}
        url = Config.FETCHEVENTS_FUNCTION_URL
        req = urllib.request.Request(url, json.dumps(data).encode(), headers)
        response = urllib.request.urlopen(req)
        return response.read()
    else:
        return """
            <html>
                <body>
                    <form method="post">
                        Start date: <input type="date" name="start_date" required><br>
                        End date: <input type="date" name="end_date" required><br>
                        Enter your email: <input type="text" name="email" required><br>
                        <input type="submit" value="Submit">
                    </form>
                </body>
            </html>
        """
