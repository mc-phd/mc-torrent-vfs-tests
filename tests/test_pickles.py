#! /usr/bin/env python3

try:
    import cPickle as pickle
except ImportError:
    import pickle

import os.path
import sys
from eff_bdecode import eff_bdecode

test_dir = os.path.dirname(__file__)
test_torrents_dir = os.path.join(test_dir, 'webtorrent-fixtures', 'fixtures')

if sys.version_info[:2] == (2, 7):
    pickles_dir = os.path.join(test_dir, 'data', 'pickles-2.7')
else:
    pickles_dir = os.path.join(test_dir, 'data', 'pickles-3')


def _test1(basename):
    torrent_file = open(os.path.join(test_torrents_dir,
                                     basename + '.torrent'), 'rb')
    torrent_data = torrent_file.read()
    torrent_file.close()

    torrent_dict = eff_bdecode(torrent_data)

    pickle_file = open(os.path.join(pickles_dir,
                                    basename + '.pickle'), 'rb')
    pickle_dict = pickle.load(pickle_file)
    pickle_file.close()

    assert torrent_dict == pickle_dict


def test_pickles():
    for basename in [
        'alice', 'bunny', 'corrupt', 'folder', 'leaves-metadata',
        'leaves', 'lots-of-numbers', 'numbers', 'sintel',
    ]:
        _test1(basename)
