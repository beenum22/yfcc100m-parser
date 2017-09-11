import bz2
import os
import sys
import argparse
import urllib
import logging

logger = logging.getLogger('flickr_dump')

class ExtractMetadata(object):
	def __init__(self, filename, output):
		self.filename = filename
		self.output = output
		try:
			self.bz2_out = bz2.BZ2File(filename, 'r')
		except IOError:
			logger.error("Failed to read '%s'" % filename)
			sys.exit()
		try:
			self.output = open(output, 'w')
		except IOError:
			logger.error("Failed to open '%s'" % output)
			sys.exit()

	def get_lines(self, start, stop):
		i = 0
		count = 0
		if stop == -1:
			stop = float("inf")
		while i < stop:
			line = self.bz2_out.readline()
			if i >= start:
				metadata = self.extract_metadata(line)
				if len(metadata) is 0 or len(line) is 0:
					logger.info("End of file")
					break
				elif metadata['longitude'] != '' and metadata['latitude'] != '' and metadata['photo_or_video'] == '0':
					#logger.info("Parsing line: %d" % i)
					self.write_metadata(metadata, count, i)
					count += 1
			i += 1

	def write_metadata(self, metadata, new_index, orig_index):
		data = "%s %s %s %s %s %s\n" % (new_index, orig_index, metadata['photo_ext'], metadata['latitude'], metadata['longitude'], metadata['url_get'])
		self.output.write(data)

	def extract_metadata(self, line):
		metadata = {}
		line = line.strip().split('\t')
		if len(line) < 25:
			return metadata
		metadata['photo_hash'] = line[2]
		metadata['user_id'] = line[3]
		metadata['user_nickname'] = line[4]
		metadata['date_taken'] = line[5]
		metadata['date_uploaded'] = line[6]
		metadata['capture_device'] = line[7]
		metadata['title'] = line[8]
		metadata['description'] = line[9]
		metadata['user_tags'] = line[10]
		metadata['machine_tags'] = line[11]
		metadata['longitude'] = line[12]
		metadata['latitude'] = line[13]
		metadata['post_accuracy'] = line[14]
		metadata['url_show'] = line[15]
		metadata['url_get'] = line[16]
		metadata['license_name'] = line[17]
		metadata['license_url'] = line[18]
		metadata['server_id'] = line[19]
		metadata['farm_id'] = line[20]
		metadata['photo_secret'] = line[21]
		metadata['photo_secret_orig'] = line[22]
		metadata['photo_ext'] = line[23]
		metadata['photo_or_video'] = line[24]
		return metadata
