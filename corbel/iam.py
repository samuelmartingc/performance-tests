import jwt
import requests
import time
import ConfigParser
from random import randint
import json

import sys
print "iammmmmmmmmmmmmmmmmmmm"
print sys.path

_LOCUST_CONFIG_FILE = 'resources/locustconfig.properties'
_MAX_EXPIRATION_TIME = 3600
config = ConfigParser.RawConfigParser()
config.read(_LOCUST_CONFIG_FILE)


def get_client_access_token(uuid, secret):
    claims = {
        'iss': uuid,
        'aud': config.get('IAM', 'iam.claims.aud'),
        'exp': time.time() + _MAX_EXPIRATION_TIME
    }

    encoded = jwt.encode(claims, secret, algorithm='HS256')

    data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": encoded
    }

    custom_headers = {
        "Content-Type":
            "application/x-www-form-urlencoded"
    }

    request = requests.post(config.get('IAM', 'iam.endpoint.gettoken'), data=data, headers=custom_headers)

    return str(request.json()['accessToken'])


_ADMIN_TOKEN = get_client_access_token(config.get('ADMIN_USER', 'admin.claims.iss'),
                                       config.get('ADMIN_USER', 'admin.secret'))


class User:
    def __init__(self):
        random = str(randint(0, 999999))
        self.email = "createUserIam.iam" + random + "@funkifake.com"
        self.username = "createUserIam.iam" + random + "@funkifake.com"
        self.password = "createUserIam.iam" + random + "@funkifake.com"

    def get_user_json(self):
        return json.dumps({"email": self.email, "username": self.username, "password": self.password})

    def set_user_id(self, id):
        self.id = id

    def set_user_access_token(self):
        self.access_token = self.get_user_access_token()

    def get_user_access_token(self):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": 'Bearer ' + _ADMIN_TOKEN,
            "withCredentials": "true"
        }

        claims = {
            "iss": config.get('ADMIN_USER', 'admin.claims.iss'),
            "aud": config.get('IAM', 'iam.claims.aud'),
            "exp": time.time() + _MAX_EXPIRATION_TIME,
            "basic_auth.username": self.username,
            "basic_auth.password": self.password,
            "scopes": ""
        }

        encoded = jwt.encode(claims, config.get('ADMIN_USER', 'admin.secret'), algorithm='HS256')

        data = {
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": encoded
        }

        request = requests.post(config.get('IAM', 'iam.endpoint.gettoken'), data=data, headers=headers)

        print request.json()
        return str(request.json()['accessToken'])

    def tostring(self):
        return self.__dict__


def create_user():
    user = User()

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": 'Bearer ' + _ADMIN_TOKEN
    }

    request = requests.post(config.get('IAM', 'iam.endpoint.createuser'), data=user.get_user_json(), headers=headers)
    user.set_user_id(request.headers['location'].split('/')[-1])
    user.set_user_access_token()

    return user


def generate_n_users(n):
    return [create_user() for _ in range(n)]


def delete_users(users):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": 'Bearer ' + _ADMIN_TOKEN
    }

    for user in users:
        request = requests.delete(config.get('IAM', 'iam.endpoint.deleteuser') + "/" + user.id, headers=headers)
        print "success!" if (request.status_code == 204) else "error! status:" + str(request.status_code)
