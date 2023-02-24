import os
from flask import (
    Flask,
    request,
    redirect,
    url_for
)
from garminconnect import (
    init_api,
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)

from wahoofitness import (
    WahooUser,
    download_workout_file
)

app = Flask(__name__)

webhook_token = os.getenv("WEBHOOK_TOKEN")
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
user_id = os.getenv("USER_ID")

# Wahoo Vars
base_url = "api.wahooligan.com"
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")

@app.route("/")
def hello_world():
    return redirect(url_for("login"))

@app.get("/login")
def login():
    auth_url = f'https://{base_url}/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=workouts_read+power_zones_read+offline_data+user_read'
    return redirect(location=auth_url)

@app.get("/redirect")
def login_redirect():
    code = request.args.get('code')
    user = WahooUser(code)
    return {
        "user_id": user.user_id
    }

@app.post("/hook")
def wahoo_hook():
    request_data = request.get_json()
    workout_summary = request_data["workout_summary"]
    workout_type = workout_summary["workout"]["workout_type_id"]
    workout_file_url = workout_summary["file"]["url"]
    user = request_data["user"]["id"]

    # Verify Request
    if(webhook_token != request_data["webhook_token"]):
        return 'Invalid Webhook Token!', 401
    if(f'{user}' != user_id):
        return 'Invalid User ID!', 401
    if(workout_type != 0 and workout_type != 15):
        return 'Unsupported Workout Type'
   
    api = init_api(email, password)
    tempfile = download_workout_file(workout_file_url)
    api.upload_activity(tempfile.name)
    tempfile.close()
    return "Done!"