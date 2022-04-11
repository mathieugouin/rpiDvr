#!/usr/bin/python3

import json
import time
import pandas as pd
import tvh_api as ta


def get_finished_recordings():
    # Large number to not be limited (default is 50)
    return ta.get_api_url('dvr/entry/grid_finished?limit=5000')


def json_pp(js):
    print(json.dumps(js, indent=4, sort_keys=False))


def _main():
    recs = get_finished_recordings()
    #json_pp(recs)

    info = []

    if recs:
        if 'total' in recs:
            print('Total number of recordings: %d' % (recs['total']))
        if 'entries' in recs:
            for r in recs['entries']:
                #print('{}\t{}'.format(r['disp_title'], r['disp_subtitle']))
                info.append({
                        'Title': r['disp_title'],
                        'Subtitle': r['disp_subtitle']
                        })

    df = pd.DataFrame(info)
    df.sort_values(list(df.columns), inplace=True)

    # print full DF
    with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.expand_frame_repr', False):
        print(df)



if __name__ == "__main__":
    _main()

