#! /usr/bin/env python3

try:
    import cPickle as pickle
except ImportError:
    import pickle

import sys
from eff_bdecode import eff_bdecode

torrent_file = open(sys.argv[1], 'rb')
torrent_data = torrent_file.read()
torrent_file.close()

torrent_dict = eff_bdecode(torrent_data)

try:
    pickle_file = open(sys.argv[2], 'rb')
except IOError:
    pickle_dict = None
else:
    pickle_dict = pickle.load(pickle_file)
    pickle_file.close()

if torrent_dict != pickle_dict:
    pickle_file = open(sys.argv[2], 'wb')
    pickle.dump(torrent_dict, pickle_file)
    pickle_file.close()
