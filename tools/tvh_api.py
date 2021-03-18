#!/usr/bin/python

# To make print working for Python2/3
from __future__ import print_function

import json
import time
import requests

TVH_SERVER = 'http://192.168.1.23:9981'


def get_api_url(api):
    url = TVH_SERVER + '/api/' + api
    ts_response = requests.get(url)
    if ts_response.status_code != 200:
        print('Error code %d\n%s' % (ts_response.status_code, ts_response.content))
        return {}
    ts_json = json.loads(ts_response.text, strict=False)
    return ts_json


def get_autorecs():
    return get_api_url('dvr/autorec/grid')


def get_idnode(uuid):
    return get_api_url('idnode/load?uuid=' + uuid)


def json_pp(js):
    print(json.dumps(js, indent=4, sort_keys=False))


def main():
    autorecs = get_autorecs()
    #json_pp(autorecs)

    if autorecs and 'entries' in autorecs:
        for e in autorecs['entries']:
            #print(e)
            #print("%s\t%s\t%s" % (e['uuid'], e['enabled'], e['name']))
            pass

    idnode = get_idnode('64a34dd9bceba0aa55066d93c9b87b3f')
    json_pp(idnode)


if __name__ == "__main__":
    main()
