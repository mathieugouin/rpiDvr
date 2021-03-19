#!/usr/bin/python3

import json
import requests
import urllib
import time


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


def set_autorec_enabled(uuid, enabled):
    js = {
        'uuid' : uuid,
        'enabled' : enabled
    }
    api = 'idnode/save?node=' + urllib.parse.quote(json.dumps(js))
    #print(api)
    return get_api_url(api)


def json_pp(js):
    print(json.dumps(js, indent=4, sort_keys=False))


def main():
    autorecs = get_autorecs()
    #json_pp(autorecs)

    enabled_uuid = []

    if autorecs and 'entries' in autorecs:
        for e in autorecs['entries']:
            if e['enabled']:
                #print("%s\t%s\t%s" % (e['uuid'], e['enabled'], e['name']))
                uuid = e['uuid']
                enabled_uuid.append(uuid)
                # disable
                set_autorec_enabled(uuid, False)

    time.sleep(3)

    for uuid in enabled_uuid:
        print("Enabling " + uuid)
        set_autorec_enabled(uuid, True)


if __name__ == "__main__":
    main()
