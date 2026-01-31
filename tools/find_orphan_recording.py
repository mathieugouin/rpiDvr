from __future__ import print_function
import json
import os
import fnmatch

# ####### KODI
TVH_BASE_DIR = '/storage/.kodi/userdata/addon_data/service.tvheadend42' # TVH config base directory
VIDEO_DIR = '/storage/DVR/recordings'

# ####### TESTING
#TVH_BASE_DIR = '/home/mgouin/Documents/Mathieu/DVR/tvh' # TVH config base directory
#VIDEO_DIR = '/home/mgouin/Documents/Mathieu/DVR/recordings_bak'

# ####### COMMON Config

TVH_DVR_DIR = TVH_BASE_DIR + '/dvr/log'

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


def get_all_video_files_from_tvh():
    video_files = set()
    for log_file in find_files(TVH_DVR_DIR, TVH_FILE_PATTERN):
        with open(log_file, 'rb') as fh_log:
            recording_data = json.load(fh_log)
            if 'files' in recording_data:
                for fdict in recording_data['files']:
                    if 'filename' in fdict:
                        video_files.add(fdict['filename'])
    return list(video_files)


def get_all_video_files_from_disk():
    video_files = set()
    for video_file in find_files(VIDEO_DIR, '*.ts'):
        video_files.add(video_file)
    return list(video_files)


def process():
    video_files_from_tvh = get_all_video_files_from_tvh()
    print("Number of video files registered in TVH logs:", len(video_files_from_tvh))
    for video_file in get_all_video_files_from_disk():
        if video_file not in video_files_from_tvh:
            print("Orphan video file found:", video_file)


def _main():
    process()


if __name__ == '__main__':
    _main()
