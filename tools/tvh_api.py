#!/usr/bin/python

# To make print working for Python2/3
from __future__ import print_function

import json
import time
import requests

TVH_SERVER = 'http://192.168.1.23:9981'


def get_api_url(api):
    return TVH_SERVER + '/api/' + api


def get_autorecs():
    ts_query = get_api_url('dvr/autorec/grid')
    ts_response = requests.get(ts_query)
    if ts_response.status_code != 200:
        print('<pre>Error code %d\n%s</pre>' % (ts_response.status_code, ts_response.content, ))
        return {}
    ts_json = json.loads(ts_response.text, strict=False)
    return ts_json


def main():
    ar = get_autorecs()

    print(ar)

    """
    timers = get_timers()
    if len(timers):
        for timer in timers:
            start = time.localtime(timer['start'])
            print('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
                % (time.strftime("%a %e/%m",start),
                   time.strftime("%H:%M",start),
                   time.strftime("%H:%M",time.localtime(timer['stop'])),
                   timer['disp_title'],
                ))
    """
                
main()
