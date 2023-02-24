import requests
import os
import tempfile

base_url = "api.wahooligan.com"
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")

def download_workout_file(file_url):
    fo = tempfile.NamedTemporaryFile()
    r = requests.get(file_url)
    fo.write(r.content)
    return fo

class WahooUser:
    def __init__(self, code=None):
        oauth = f'https://{base_url}/oauth/token?client_secret={client_secret}&code={code}&redirect_uri={redirect_uri}&grant_type=authorization_code&client_id={client_id}'
        r = requests.post(oauth)
        print(r.text)
        self.access_token = r.json()["access_token"]
        self.refresh_token = r.json()["refresh_token"]
        self.user_id = self.get_user()

    def get_user(self):
        # --header "Authorization: Bearer users-token-goes-here"
        headers = {
            "Authorization": f'Bearer {self.access_token}'
        }
        user_url = f'https://{base_url}/v1/user'
        r = requests.get(user_url, headers=headers)
        return r.json()["id"]
