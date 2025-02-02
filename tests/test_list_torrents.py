#! /usr/bin/env python3

from datetime import datetime, timedelta
from time import mktime, timezone
import os
import os.path
import subprocess
import sys

os.environ['TZ'] = 'GMT'  # Fix timezone for date/time comparison

test_dir = os.path.dirname(__file__)
expected_dir = os.path.join(test_dir, 'data', 'expected')
extfs_dir = os.path.join(test_dir, 'extfs.d')
test_torrents_dir = os.path.join(test_dir, 'webtorrent-fixtures', 'fixtures')


def _get_filename(line):
    return line.split(None, 7)[7]


def _test1(basename):
    torrent_file = os.path.join(test_torrents_dir, basename + '.torrent')

    if basename == 'leaves-metadata':
        # The torrent lacks creation_date field, set fixd timestamp
        leaves_metadata_dt = datetime(2016, 3, 16, 19, 33)
        if (sys.version_info[:2] <= (3, 7)) and \
                (sys.platform == 'win32'):
            leaves_metadata_dt -= timedelta(seconds=timezone)
        timestamp = mktime(leaves_metadata_dt.timetuple())
        os.utime(torrent_file, (timestamp, timestamp))

    command = os.path.join(extfs_dir, 'torrent')
    pipe = subprocess.Popen([sys.executable, command, 'list', torrent_file],
                            stdout=subprocess.PIPE)
    torrent_list = pipe.stdout.read()
    pipe.stdout.close()
    if basename == 'corrupt':
        assert pipe.wait() == 1  # result=1, Error
    else:
        assert pipe.wait() == 0  # result=0, Ok
        torrent_list_lines = torrent_list.splitlines()
        torrent_list_lines.sort(key=_get_filename)
        expected_file = open(os.path.join(expected_dir, basename + '.txt'),
                             'rb')
        expected_lines = [line.strip() for line in expected_file.readlines()]
        expected_file.close()
        assert torrent_list_lines == expected_lines


def test_list_torrents():
    for basename in [
        'alice', 'bunny', 'corrupt', 'folder', 'leaves-metadata',
        'leaves', 'lots-of-numbers', 'numbers', 'sintel',
    ]:
        _test1(basename)
