# ref: https://github.com/dave-p/TVH-API-docs/wiki

import json
import urllib.request
import urllib.parse

_TVH_SERVER = 'http://192.168.1.23:9981'


# Debug utils
def json_pp(js):
    print(json.dumps(js, indent=4, sort_keys=False))


def get_api_url(api, params=None):
    url = _TVH_SERVER + '/api/' + api
    if params is not None:
        url += "?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                print('Error code %d\n%s' % (response.status, response.read().decode('utf-8')))
                return {}
            data = response.read().decode('utf-8')
            ts_json = json.loads(data, strict=False)
            return ts_json
    except urllib.error.HTTPError as e:
        print('HTTPError: %d\n%s' % (e.code, e.read().decode('utf-8')))
    except urllib.error.URLError as e:
        print('URLError:', e.reason)
    return {}


def _main():
    print(json.dumps(get_api_url('serverinfo'), indent=4))


if __name__ == "__main__":
    _main()
