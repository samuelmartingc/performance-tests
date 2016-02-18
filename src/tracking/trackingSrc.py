import requests
import ConfigParser
import json

import sys
print "trakinnnnnnnnnnnnnnnnnnnnnn"
print sys.path

_LOCUST_CONFIG_FILE = 'resources/locustconfig.properties'

config = ConfigParser.RawConfigParser()
config.read(_LOCUST_CONFIG_FILE)


def send_tracking(user):
    print "hola"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": 'Bearer ' + user.access_token
    }

    request = requests.post(config.get('TRACKING', 'tracking.progress.endpoint'),
                            data=json.dumps(config.get('TRACKING', 'tracking.progress.data')),
                            headers=headers)

    print request.status_code
