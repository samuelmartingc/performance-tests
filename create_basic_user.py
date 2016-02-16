from locust import HttpLocust, TaskSet
from random import randint
import jwt
import json
import requests
import time
import ConfigParser

_LOCUST_CONFIG_FILE = 'locustconfig.properties'


def generate_random_user():
    random = str(randint(0, 999999))
    email = "createUserIam.iam" + random + "@funkifake.com"
    username = "createUserIam.iam" + random + "@funkifake.com"
    return json.dumps({"email": email, "username": username})


def get_access_token():
    config = ConfigParser.RawConfigParser()
    config.read(_LOCUST_CONFIG_FILE)

    claims = {
        'iss': config.get('ADMIN_USER', 'admin.claims.iss'),
        'aud': config.get('ADMIN_USER', 'admin.claims.aud'),
        'exp': time.time() + 100
    }

    encoded = jwt.encode(claims, config.get('ADMIN_USER', 'admin.secret'), algorithm='HS256')

    data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": encoded
    }

    custom_headers = {
        "Content-Type":
            "application/x-www-form-urlencoded"
    }

    request = requests.post('http://localhost:8082/v1.0/oauth/token', data=data, headers=custom_headers)
    return str(request.json()['accessToken'])


def create_user(l):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": 'Bearer ' + get_access_token()
    }

    response = l.client.post("/v1.0/user", data=generate_random_user(), headers=headers)

    print "Response status code:", response.status_code
    print "Response content:", response.content


class UserBehavior(TaskSet):
    tasks = {create_user: 1}


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
