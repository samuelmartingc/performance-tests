import ConfigParser
import json

_LOCUST_CONFIG_FILE = 'resources/locustconfig.properties'

config = ConfigParser.RawConfigParser()
config.read(_LOCUST_CONFIG_FILE)


def send_tracking(l, user):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": 'Bearer ' + user.access_token
    }

    l.client.post(url=config.get('TRACKING', 'tracking.tracking.endpoint'),
                             data=json.dumps(config.get('TRACKING', 'tracking.tracking.data')),
                             headers=headers)

