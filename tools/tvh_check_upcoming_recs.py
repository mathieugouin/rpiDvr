#!/usr/bin/python3

import time
import datetime
import pandas as pd
import tvh_api as ta

MAX_CONCURRENT_RECORDING = 2


def get_upcoming_recs():
    # Large number to not be limited (default is 50)
    return ta.get_api_url('dvr/entry/grid_upcoming', {'limit': 5000})


def get_channels():
    # Large number to not be limited (default is 50)
    return ta.get_api_url('channel/grid', {'limit': 5000})


def get_channel_name(channels, uuid):
    j = channels
    if 'entries' in j:
        for e in j['entries']:
            if e['uuid'] == uuid:
                return e['name']
    return ''


def to_timestamp(t):
    return datetime.datetime.fromtimestamp(time.mktime(time.localtime(t)))


def get_df():
    channels = get_channels()
    js = get_upcoming_recs()

    df = None

    info = []

    if js:
        if 'entries' in js:
            for e in js['entries']:
                # Example:

                """
                {
                    "uuid": "f57f99dce3fb33461cecdac94fe8b373",
                    "enabled": true,
                    "start": 1691055000,
                    "start_extra": 0,
                    "start_real": 1691054970,
                    "stop": 1691056800,
                    "stop_extra": 0,
                    "stop_real": 1691056800,
                    "duration": 1800,
                    "channel": "ce5e518cf16b175659fdde6eee846a95",
                    "channel_icon": "https://raw.githubusercontent.com/mathieugouin/rpiDvr/master/zap2xml/iconsMan/tva.png",
                    "channelname": "TVA",
                    "title": {
                        "eng": "Les looney tunes"
                    },
                    "disp_title": "Les looney tunes",
                    "disp_subtitle": "",
                    "description": {
                        "eng": "Les aventures de Bugs Bunny, Daffy Duck, Porky Pig et leurs amis."
                    },
                    "disp_description": "Les aventures de Bugs Bunny, Daffy Duck, Porky Pig et leurs amis.",
                    "pri": 2,
                    "retention": 0,
                    "removal": 0,
                    "playposition": 0,
                    "playcount": 0,
                    "config_name": "8d0f5b7ae354d956d7fe5db25f5d0d24",
                    "creator": "192.168.1.51",
                    "filename": "",
                    "directory": "Les-looney-tunes",
                    "errorcode": 0,
                    "errors": 0,
                    "data_errors": 0,
                    "dvb_eid": 0,
                    "noresched": false,
                    "norerecord": false,
                    "fileremoved": 0,
                    "autorec": "3bd5dfe7e8bbe2f5eb10e8cda8c5b127",
                    "autorec_caption": "Les looney tunes (Les looney tunes)",
                    "timerec": "",
                    "timerec_caption": "",
                    "parent": "",
                    "child": "",
                    "content_type": 5,
                    "broadcast": 890920,
                    "url": "",
                    "filesize": 0,
                    "status": "Scheduled for recording",
                    "sched_status": "scheduled",
                    "duplicate": 0,
                    "comment": "Auto recording: Les looney tunes"
                }
                """

                # ta.json_pp(e)

                if e['enabled']:

                    info.append({
                            'Title': e['disp_title'],
                            'Channel': get_channel_name(channels, e['channel']),

                            'Start': to_timestamp(e['start']),
                            'Stop': to_timestamp(e['stop']),

                            # 'Duration (min)': e['duration'] / 60.0,
                            })

        df = pd.DataFrame(info)
        #                                              At equal start time, longer 1st
        df.sort_values(by=['Start', 'Stop'], ascending=[True, False], inplace=True, ignore_index=True)

        df['Duration'] = df['Stop'] - df['Start']

        df.rename_axis('ATTRIBUTES', axis='columns', inplace=True)
        df.rename_axis('INDEX', axis='index', inplace=True)

        return df


def analyze_df(df):
    # Many possibilities:
    #
    # ref rec:          ************                   : comp overlap ref?
    # comp rec:   ----                                 : n
    #              --------                            : y
    #              ---------------------               : y
    #                   ------------                   : y
    #                      ------                      : y
    #                         ------------             : y
    #                                 -------------    : n
    #
    # Loop on the df and store the start & stop time in a new df,
    # in the same column with a column attribute indicating start (1) or stop (0).
    # Store also the recording Index from the original df.
    data = []
    for index, row in df.iterrows():
        data.append([row['Start'], 1, index])
        data.append([row['Stop'], 0, index])

    dfa = pd.DataFrame(data=data, columns=['Time', 'Type', 'RecIndex'])
    dfa.sort_values(by=['Time', 'Type', 'RecIndex'], ascending=[True, True, True], inplace=True, ignore_index=True)
    dfa.rename_axis('ATTRIBUTES', axis='columns', inplace=True)
    dfa.rename_axis('INDEX', axis='index', inplace=True)

    # Loop on the analysis df and use a stack to push when start time, pop when stop time
    dfr = df.copy()
    dfr['NbTunerRequired'] = 0
    recording_stack = []
    for index, row in dfa.iterrows():
        if row['Type'] > 0:  # Start: one more tuner used.
            recording_stack.append(row['RecIndex'])
            dfr.loc[recording_stack, 'NbTunerRequired'] = len(recording_stack)  # Equivalent of the nb of tuner used
            if len(recording_stack) > MAX_CONCURRENT_RECORDING:
                print('--------------------------------------------------')
                print(dfr.loc[recording_stack])
        else:
            _ = recording_stack.pop()

    return dfr[dfr['NbTunerRequired'] > MAX_CONCURRENT_RECORDING]


def _main():
    df = get_df()

    df2 = analyze_df(df)

    if not df2.empty:
        print("The following upcoming recording(s) will not be possible with %d tuner(s)" % MAX_CONCURRENT_RECORDING)

        # print full DF
        with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.expand_frame_repr', False):
            print(df2)

    else:
        print("All upcoming recording(s) will be possible with %d tuner(s)" % MAX_CONCURRENT_RECORDING)


if __name__ == "__main__":
    _main()
