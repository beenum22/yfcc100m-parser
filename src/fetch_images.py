import urllib
import logging
import sys

logger = logging.getLogger('flickr_dump')


class FetchImages(object):
	def __init__(self, fileName, outDir):
		self.fileName = fileName
		self.outDir = outDir
		try:
			logger.info("Reading the %s" % fileName)
			self.file = open(fileName, 'r')
		except IOError:
			logger.error("Failed to read '%s'" % fileName)
			sys.exit()

	def read_file(self, start, stop):
		i = 0
		count = 0
		if stop == -1:
			stop = float("inf")
		while i < stop:
			line = self.file.readline()
			if len(line) is 0:
				logger.info("End of file")
				break
			if i >= start:
				#logger.info("Parsing line: %d" % i)
				self.download_image(line)
			i += 1

	def download_image(self, line):
		lineList = line.split()
		imagePath = "%simage_%s.%s" % (self.outDir, lineList[0], lineList[2])
		logger.info("Downloading the image from %s" % imagePath)
		try:
			urllib.urlretrieve(lineList[5], imagePath)
		except:
			logger.error("Failed to fetch the image_%s from '%s'" % (lineList[0], lineList[5]))

