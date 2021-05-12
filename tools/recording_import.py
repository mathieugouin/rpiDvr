#!/usr/bin/python

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import json
import random
import os
import fnmatch
import subprocess
import math
import collections

# ####### KODI
TVH_BASE_DIR = '/storage/.kodi/userdata/addon_data/service.tvheadend42' # TVH config base directory
VIDEO_DIR = '/storage/DVR/recordings_backup'
TEMP_DIR = '/storage/tmp/dvr'

# ####### TESTING
#TVH_BASE_DIR = '/home/mgouin/Documents/Mathieu/DVR/tvh' # TVH config base directory
#VIDEO_DIR = '/home/mgouin/Documents/Mathieu/DVR/recordings_bak'
#TEMP_DIR = '/home/mgouin/tmp/dvr'

# ####### COMMON Config

# /storage/.kodi/userdata/addon_data/service.tvheadend42/dvr/log
TVH_DVR_DIR = TVH_BASE_DIR + '/dvr/log'
TVH_CONFIG_DIR = TVH_BASE_DIR + '/dvr/config'
TVH_CHANNEL_DIR = TVH_BASE_DIR + '/channel/config'

TVH_FILE_PATTERN = "????????????????????????????????"

# TODO: The following constants need to be updated according to the TVH install: 
TVH_CONFIG_NAME = "8d0f5b7ae354d956d7fe5db25f5d0d24" # Look for the file name inside TVH_BASE_DIR + 'dvr/config'
TVH_DEFAULT_CHANNEL_KEY = '52cf67a489e79fdb75b9081e5ee8865e' # Look for any file name inside TVH_BASE_DIR + 'channel/config'
TVH_DEFAULT_CHANNEL_NAME = 'Radio-Canada' # Pick the corresponding name of the chosen file

START_TIME_RESOLUTION = 30.0 * 60.0 # in seconds
DURATION_RESOLUTION = 60.0 # in seconds

def roundup(x, r):
    return math.ceil(float(x) / r) * r

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


def test():
    print subprocess.check_output(["pwd"])
    print subprocess.check_output(["echo", "hey you!"])
    print subprocess.check_output(["ls"])
    print subprocess.check_output(['ls'])
    print subprocess.check_output(['git', '--version'])
    return
    for f in find_files('/home/mgouin/Documents/Mathieu/DVR/tvh', '????????????????????????????????'):
        print f


# Empty string when at root
def get_video_directory(video_file):
    basedir = os.path.split(os.path.relpath(video_file, VIDEO_DIR))[0]
    return basedir

def get_video_duration(video_file):
    # Need to install the ffmpeg-tools addon
    # https://ffmpeg.org/ffprobe.html#Options
    # ffprobe -v quiet -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 filename.ts
    output = subprocess.check_output([
        "ffprobe",
        "-v",
        "quiet",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        video_file])
    return float(output.strip())


# Create a new filename for dvr log, with leading 0s
def get_new_filename():
    return "{:032x}".format(random.getrandbits(128))


def process():
    # get all existing tvh recordings (to prevent accidental duplication of filename)
    existing_recording_logs = [os.path.relpath(f, TVH_DVR_DIR) for f in find_files(TVH_DVR_DIR, TVH_FILE_PATTERN)]

    for video_file in find_files(VIDEO_DIR, "*.ts"):
        print "Processing", video_file

        video_directory = get_video_directory(video_file)

        log_name = get_new_filename()
        # Generate a new name in case already present (low probability)
        while log_name in existing_recording_logs:
            log_name = get_new_filename()

        # getmtime return in seconds, round down to a decent resolution
        video_mod_time = roundup(os.path.getmtime(video_file), START_TIME_RESOLUTION)
        video_duration = roundup(get_video_duration(video_file), DURATION_RESOLUTION)

        title = os.path.splitext(os.path.basename(video_file))[0]

        recordingDict = collections.OrderedDict()
        startTime = video_mod_time
        stopTime = startTime + int(video_duration)
        recordingDict['enabled'] = True
        recordingDict['start'] = startTime
        recordingDict['start_extra'] = 0
        recordingDict['stop'] = stopTime
        recordingDict['stop_extra'] = 0
        recordingDict['channel'] = TVH_DEFAULT_CHANNEL_KEY
        recordingDict['channelname'] = TVH_DEFAULT_CHANNEL_NAME
        recordingDict['title'] = { 'eng': title }
        recordingDict['description'] = { 'eng': 'Recording auto imported from script' }
        recordingDict['pri'] =  2
        recordingDict['retention'] = 0
        recordingDict['removal'] = 0
        recordingDict['playposition'] = 0
        recordingDict['playcount'] = 0
        recordingDict['config_name'] = TVH_CONFIG_NAME
        recordingDict['creator'] = 'Rebuild'
        if video_directory:
            recordingDict['directory'] = video_directory

        recordingDict['errorcode'] = 0
        recordingDict['errors'] = 0
        recordingDict['data_errors'] = 0
        recordingDict['dvb_eid'] = 0
        recordingDict['noresched'] = True
        recordingDict['norerecord'] = False
        recordingDict['fileremoved'] = 0
        recordingDict['autorec'] = ''
        recordingDict['timerec'] = ''
        recordingDict['parent'] = ''
        recordingDict['child'] = ''
        recordingDict['content_type'] = 0
        recordingDict['broadcast'] = 0
        recordingDict['comment'] = 'Recording auto imported from script'

        recordingDict['files'] = list()
        recordingDict['files'].append({'filename': video_file})

        outFileName = os.path.join(TVH_DVR_DIR, log_name)  # real
        #outFileName = os.path.join(TEMP_DIR, log_name)     # testing

        if not os.path.exists(TEMP_DIR):
            raise 'BAD'
            return
        with open(outFileName, 'wb') as fh_log:
            json.dump(recordingDict, fh_log, indent=4)
            fh_log.write('\n')
            print '  => Created:', outFileName


def _main():
    process()
    #test()


if __name__ == '__main__':
    _main()
