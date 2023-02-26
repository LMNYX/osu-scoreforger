import requests
import random
import string


class AccountForger:
    def __init__(self):
        pass

    def random_string(self):
        return ''.join(random.choice(string.ascii_letters) for i in range(8))

    def random_str(self, much):
        return ''.join(random.choice(string.ascii_letters) for i in range(much))

    def forge(self, username, password):
        data_headers = {"charset": "utf-8"}
        data = {
            "user[username]": (None, username, "text/plain", data_headers),
            "user[password]": (None, password, "text/plain", data_headers),
            "user[user_email]": (None, username + "@gmail.com", "text/plain", data_headers)
        }

        r = requests.post("https://osu.ppy.sh/users", files=data, headers={
            "User-Agent": "osu!"
        })

        if r.status_code == 200:
            return {"username": username, "password": password}

    def oauth_auth(self, username, password):
        data_headers = {"charset": "utf-8"}
        data = {
            "username": (None, username, "text/plain", data_headers),
            "password": (None, password, "text/plain", data_headers),
            "grant_type": (None, "password", "text/plain", data_headers),
            "client_id": (None, 5, "text/plain", data_headers),
            "client_secret": (None, "FGc9GAtyHzeQDshWP5Ah7dega8hJACAJpQtw6OXk", "text/plain", data_headers),
            "scope": (None, "*", "text/plain", data_headers)
        }

        r = requests.post("https://osu.ppy.sh/oauth/token",
                          files=data, headers={"User-Agent": "osu!"})

        if r.status_code == 200:
            return r.json()["access_token"]
        else:
            return None

    def forge_random(self):
        username = f"VERIFYSCORES_{self.random_str(2)}"
        password = self.random_str(8)
        email = f"{self.random_str(8)}@gmail.com"

        acc = self.forge(username, password)
        oauth = self.oauth_auth(username=username, password=password)

        if acc and oauth:
            return {"username": username, "password": password, "email": email, "oauth": oauth}
        else:
            return None


ac = AccountForger()
x = ac.forge_random()
print(x)
