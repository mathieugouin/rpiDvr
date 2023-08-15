#!/usr/bin/python3

import pandas as pd
import tvh_api as ta
import re


def get_autorecs():
    # Large number to not be limited (default is 50)
    return ta.get_api_url('dvr/autorec/grid', {'limit': 5000})


def get_channels():
    # Large number to not be limited (default is 50)
    return ta.get_api_url('channel/grid', {'limit': 5000})


def is_dir_name_ok(d):
    try:
        d.decode('ascii') if isinstance(d, bytes) else d.encode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        if re.match(r'^[-0-9A-Z_a-z]+$', d):
            return True
        else:
            return False


def get_channel_name(channels, uuid):
    j = channels
    if 'entries' in j:
        for e in j['entries']:
            if e['uuid'] == uuid:
                return e['name']
    return ''


def get_df():
    channels = get_channels()
    autorecs = get_autorecs()

    df = None

    info = []

    if autorecs:
        # ta.json_pp(autorecs)

        # if 'total' in autorecs:
        #     print('Total number of autorecs: %d' % (autorecs['total']))

        if 'entries' in autorecs:
            for a in autorecs['entries']:
                # Example:
                """
                {
                    "uuid": "b803e4b58c67683d8cd3cafc7a3eb0a6",
                    "enabled": true,
                    "name": "Une affaire criminelle",
                    "directory": "Une-affaire-criminelle",
                    "title": "Une affaire criminelle",
                    "fulltext": false,
                    "channel": "43bd2daafc3b4ee9a460ce48909673eb",
                    "tag": "",
                    "btype": 0,
                    "content_type": 0,
                    "start": "Any",
                    "start_window": "Any",
                    "start_extra": 0,
                    "stop_extra": 0,
                    "weekdays": [
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7
                    ],
                    "minduration": 0,
                    "maxduration": 0,
                    "pri": 2,
                    "record": 0,
                    "retention": 0,
                    "removal": 0,
                    "maxcount": 0,
                    "maxsched": 0,
                    "config_name": "8d0f5b7ae354d956d7fe5db25f5d0d24",
                    "brand": "",
                    "season": "",
                    "serieslink": "",
                    "creator": "192.168.1.51",
                    "comment": "Une affaire criminelle"
                },
                """
                # print('{}\t{}'.format(a['disp_title'], a['disp_subtitle']))
                info.append({
                        'Name': a['name'],
                        'Title': a['title'],
                        'Directory': a['directory'],
                        'Channel': get_channel_name(channels, a['channel']),
                        'Comment': a['comment'],
                        'Enabled': a['enabled'],
                        })

        df = pd.DataFrame(info)
        df.sort_values(list(df.columns), inplace=True, ignore_index=True)

        return df


def _main():
    df = get_df()

    df['DirOk'] = df['Directory'].apply(is_dir_name_ok)

    # print full DF
    with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.expand_frame_repr', False):
        print(df)


if __name__ == "__main__":
    _main()
