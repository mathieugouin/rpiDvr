#!/usr/bin/python3

# ref: https://github.com/dave-p/TVH-API-docs/wiki

import json
import urllib
import time
import tvh_api as ta


def get_autorecs():
    # Large number to not be limited (default is 50)
    return ta.get_api_url('dvr/autorec/grid', {'limit': 5000})


def set_autorec_enabled(uuid, enabled):
    js = {
        'uuid' : uuid,
        'enabled' : enabled
    }
    return ta.get_api_url('idnode/save', {'node': json.dumps(js)})


def _main():
    autorecs = get_autorecs()
    #ta.json_pp(autorecs)

    enabled_uuid = []
    count = 0

    if autorecs:
        if 'total' in autorecs:
            print('Total number of autorecs: %d' % (autorecs['total']))
        if 'entries' in autorecs:
            for e in autorecs['entries']:
                #if True:
                if e['enabled']:
                    print("%s\t%s\t%s" % (e['uuid'], e['enabled'], e['name']))
                    uuid = e['uuid']
                    enabled_uuid.append(uuid)
                    time.sleep(0.1)
                    set_autorec_enabled(uuid, False)
                    count += 1

    print("========================================================")
    print("Disabled %d enabled autorecs" % (count))
    print("========================================================")

    for uuid in enabled_uuid:
        print("Enabling " + uuid)
        set_autorec_enabled(uuid, True)
        time.sleep(0.1)


if __name__ == "__main__":
    _main()
