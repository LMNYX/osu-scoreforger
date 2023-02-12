import requests
import random
import hashlib
import os
from dotenv import load_dotenv
load_dotenv()

# versionhash: 6bdb52cccf7f0fb48fac2f4a4f446f24

bit32limit = 2147483647
bit16limit = 65535
bit8limit = 255
bit4limit = 15
bit2limit = 3
bit1limit = 1


class RuleSets:
    STANDARD = 0
    TAIKO = 1
    CATCH = 2
    MANIA = 3


class PassState:
    PASS = True
    FAIL = False


class Ranks:
    SSH = "XH"
    SS = "X"
    SH = "SH"
    S = "S"
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    F = "F"


def BuildModsArray(*mods):
    mods_array = []
    for mod in mods:
        mods_array.append({"acronym": mod})

    return mods_array


def random_between(min, max):
    return random.randint(min, max)


class ScoreData:
    def __init__(self, ruleset_id, passed, total_score, accuracy, max_combo, rank, mods, statistics, maximum_statistics):
        self.ruleset_id = ruleset_id
        self.passed = passed
        self.total_score = total_score
        self.accuracy = accuracy
        self.max_combo = max_combo
        self.rank = rank
        self.mods = mods
        self.statistics = statistics
        self.maximum_statistics = maximum_statistics

        data = {
            "ruleset_id": self.ruleset_id,
            "passed": self.passed,
            "total_score": self.total_score,
            "accuracy": self.accuracy,
            "max_combo": self.max_combo,
            "rank": self.rank,
            "mods": self.mods,
            "statistics": self.statistics,
            "maximum_statistics": self.maximum_statistics
        }

        self.data = data


class ScoreForger:

    def __init__(self, login, password, version_hash):
        self.version_hash = version_hash
        self.client_id = 5
        self.client_secret = 'FGc9GAtyHzeQDshWP5Ah7dega8hJACAJpQtw6OXk'
        self.login = login
        self.password = password
        self.token = self.auth(login, password)

    def auth(self, login, password):
        data_headers = {"charset": "utf-8"}
        data = {
            "username": (None, login, "text/plain", data_headers),
            "password": (None, password, "text/plain", data_headers),
            "grant_type": (None, "password", "text/plain", data_headers),
            "client_id": (None, self.client_id, "text/plain", data_headers),
            "client_secret": (None, self.client_secret, "text/plain", data_headers),
            "scope": (None, "*", "text/plain", data_headers)
        }
        r = requests.post('https://osu.ppy.sh/oauth/token', files=data)

        if r.status_code == 200:
            return r.json()['access_token']
        else:
            raise Exception('Auth failed: ' + r.text)

    def get_beatmap(self, beatmap_id):
        data_headers = {
            "charset": "utf-8",
            "Authorization": "Bearer " + self.token,
            "User-Agent": "osu!",
            "Accept": "application/json",
            'Cookie': 'INGRESSCOOKIE=1672208432.33.39.918840|3895cf8eddf4633e9068ff729427d3e6'
        }

        r = requests.get('https://osu.ppy.sh/api/v2/beatmaps/' +
                         str(beatmap_id), headers=data_headers)

        if r.status_code == 200:
            return r.json()
        else:
            raise Exception('Beatmap dump failed: ' + r.text)

    def create_score(self, beatmap_id, ruleset_id):
        ez_headers = {"charset": "utf-8"}
        data_headers = {
            "charset": "utf-8",
            "Authorization": "Bearer " + self.token,
            "User-Agent": "osu!",
            "Accept": "application/json",
            'Cookie': 'INGRESSCOOKIE=1672208432.33.39.918840|3895cf8eddf4633e9068ff729427d3e6'
        }

        checksum = self.get_beatmap(beatmap_id)['checksum']

        data = {
            "version_hash": (None, self.version_hash, "text/plain", ez_headers),
            "beatmap_hash": (None, checksum, "text/plain", ez_headers),
            "ruleset_id": (None, str(ruleset_id), "text/plain", ez_headers)
        }

        r = requests.post('https://osu.ppy.sh/api/v2/beatmaps/' +
                          str(beatmap_id) + '/solo/scores', files=data, headers=data_headers)

        if r.status_code == 200:
            return r.json()
        else:
            raise Exception('Score creation failed: ' +
                            f"[{r.status_code}]" + r.text)

    def submit_score(self, score, scoredata):
        data_headers = {
            "charset": "utf-8",
            "Authorization": "Bearer " + self.token,
            "User-Agent": "osu!",
            "Accept": "application/json",
            'Cookie': 'INGRESSCOOKIE=1672208432.33.39.918840|3895cf8eddf4633e9068ff729427d3e6'
        }

        data = scoredata.data

        r = requests.put('https://osu.ppy.sh/api/v2/beatmaps/' +
                         str(score['beatmap_id']) + '/solo/scores/' + str(score['id']), json=data, headers=data_headers)
        if r.status_code == 200:
            return r.json()
        else:
            raise Exception('Submission failed: ' + r.text)

    def send_message(self, user_id, message):
        data_headers = {
            "charset": "utf-8", "Authorization": "Bearer " + self.token, "User-Agent": "osu!", "Accept": "application/json", 'Cookie': 'INGRESSCOOKIE=1672208432.33.39.918840|3895cf8eddf4633e9068ff729427d3e6'}
        data = {"message": message}
        r = requests.post('https://osu.ppy.sh/api/v2/chat/users/' +
                          str(user_id) + '/new', json=data, headers=data_headers)

        if r.status_code == 200:
            return r.json()
        else:
            raise Exception('Message sending failed: ' + r.text)


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_osu_runtime_dir():
    winusername = os.getlogin()

    base_directory = "C:\\Users\\" + winusername + "\\AppData\\Local\\osulazer\\"

    if not os.path.exists(base_directory):
        print("osu!lazer directory not found!")
        exit(1)

    directory = os.listdir(base_directory)
    directory.sort(key=lambda x: os.path.getmtime(base_directory + x))
    directory = [x for x in directory if "packages" not in x]
    directory = [x for x in directory if os.path.isdir(base_directory + x)]
    directory = directory[-1]

    return base_directory + directory
