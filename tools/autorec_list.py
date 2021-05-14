#!/usr/bin/python

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import json
import os
import fnmatch
import collections
import pandas as pd

# ####### KODI
#TVH_BASE_DIR = '/storage/.kodi/userdata/addon_data/service.tvheadend42' # TVH config base directory

# ####### TESTING
TVH_BASE_DIR = '/home/mgouin/tmp/tvh'

# ####### COMMON Config

# /storage/.kodi/userdata/addon_data/service.tvheadend42/dvr/log
TVH_AUTOREC_DIR = TVH_BASE_DIR + '/dvr/autorec'
TVH_CHANNEL_DIR = TVH_BASE_DIR + '/channel/config'

TVH_FILE_PATTERN = "????????????????????????????????"

# Will always return absolute path to files matched
def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                # Abs path
                filename = os.path.join(root, basename)
                # Optional: relative path from directory
                #filename = os.path.relpath(filename, directory)
                yield filename


def get_channel_dict():
    d = {}
    for f in find_files(TVH_CHANNEL_DIR, TVH_FILE_PATTERN):
        #print f
        fname = os.path.split(f)[1]
        #print fname
        with open(f) as fh:
            chan_data = json.load(fh)
            #print json.dumps(chan_data, indent=4, sort_keys=False)
            d[fname] = chan_data['name']

    #print d
    return d


def process():
    # Get channel dict
    ch_dict = get_channel_dict()
    #print ch_dict

    # Get all autorecs
    ar = []
    for f in find_files(TVH_AUTOREC_DIR, TVH_FILE_PATTERN):
        #print f
        with open(f) as fh:
            ar_data = json.load(fh)
            #print json.dumps(ar_data, indent=4, sort_keys=False)
            ar_dict = {}
            for k in ['name', 'title', 'directory']:
                if k in ar_data:
                    ar_dict[k] = ar_data[k]
                else:
                    ar_dict[k] = ''
            ch = ar_data['channel']
            if ch in ch_dict:
                ar_dict['channel'] = ch_dict[ch]
            else:
                ar_dict['channel'] = ''
            ar.append(ar_dict)

    df = pd.DataFrame(ar)
    df.sort_values('channel', inplace=True)
    # No wrap when printing
    pd.set_option('display.expand_frame_repr', False)
    print df


def _main():
    process()


if __name__ == '__main__':
    _main()
