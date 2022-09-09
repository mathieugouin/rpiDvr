# ref: https://github.com/dave-p/TVH-API-docs/wiki

import json
import requests
import urllib

_TVH_SERVER = 'http://192.168.1.23:9981'


# Debug utils
def json_pp(js):
    print(json.dumps(js, indent=4, sort_keys=False))


def get_api_url(api):
    url = _TVH_SERVER + '/api/' + api
    ts_response = requests.get(url)
    if ts_response.status_code != 200:
        print('Error code %d\n%s' % (ts_response.status_code, ts_response.content))
        return {}
    ts_json = json.loads(ts_response.text, strict=False)
    return ts_json


