#!/usr/bin/env python
__author__ = 'Muneeb'
__version__ = '1.0'

import os
import sys
import argparse
from src.extract_metadata import ExtractMetadata
from src.fetch_images import FetchImages
import logging
import time

logger = logging.getLogger('flickr_dump')
formatter = logging.Formatter('[YFCC100m_v' + __version__ +'] %(levelname)s:%(asctime)s:%(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

class RunTest(object):
	logger.info("Initiating program")
	parser = argparse.ArgumentParser(description='Parse the yfcc100m dataset', version=__version__)
	exclusive_group = parser.add_mutually_exclusive_group(required=True)
	required_group = parser.add_argument_group('Required Parameters')
	optional_group = parser.add_argument_group('Optional Parameters')
	required_group.add_argument('-f', '--filename', required=True, help='Name of the dataset file')
	optional_group.add_argument('--start', help='Starting line of the dataset file (default = 0)', default='0', type=int)
	optional_group.add_argument('--end', help='Ending line of the dataset/new_metadata file (default = 8, input -1 for the last line)', default='8', type=int)
	optional_group.add_argument('--path', help='Images directory (default = current directory)', default='output/')
	optional_group.add_argument('--out', help='Metadata text file (default = metadata.txt)', default='metadata.txt')
	exclusive_group.add_argument("--extract", help="Extract information from metadata", action="store_true")
	exclusive_group.add_argument("--download", help="Download images", action="store_true")
	required_group.add_argument("--debug", help="Add verbosity to the output", action="store_true")
	args = parser.parse_args()
	if args.debug:
		logger.setLevel(logging.DEBUG)
	else:
		logger.setLevel(logging.ERROR)
	t1 = time.time()
	if args.extract:
		logger.info("Extracting information from metadata")
		out = ExtractMetadata(args.filename, args.out)
		out.get_lines(args.start, args.end)
		out.bz2_out.close()
		out.output.close()
	elif args.download:
		fetch = FetchImages(args.filename, args.path)
		fetch.read_file(args.start, args.end)
		fetch.file.close()
	timeDiff = time.time() - t1
	#logger.info("Time elapsed: %d sec" % timeDiff)
	print "Time elapsed: %d sec" % timeDiff

if __name__ == '__main__':
	RunTest()

