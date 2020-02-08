from os import walk, path, startfile, listdir, remove
from codecs import open
from PyQt5.QtCore import QObject, qDebug, QDateTime
from time import time


class LogPrintFile(QObject):
	"""."""
			
	def __init__(self, logpath , logname = 'noname', printlog = True, days = 0, parent=None):
		"""Init."""
		super(LogPrintFile, self).__init__(parent)
		self.parent = parent
		self.daysDelFile = days
		self.printlog = printlog
		self.logPathFile = logpath
		self.logFileName = QDateTime.currentDateTime().toString('yyMMddhhmmss') + "_" + logname + ".log"
		self.logFileName = path.join(self.logPathFile, self.logFileName)
		qDebug('log file :' + self.logFileName)
		if days > 0:
			self.purge_logfiles()

	def write_log_file(self, operation, line, modification = True, writeconsole = True):
		"""Write log file."""
		if modification:
			logline = '{:>22} : {}  '.format(operation, line)
		else:
			if line == "":
				logline = operation + "\n"
			else:
				logline = '{} "{}"'.format(operation, line)
		text_file = open(self.logFileName, "a", 'utf-8')
		text_file.write(logline+"\n")
		text_file.close()
		if writeconsole or self.printlog:
			print(logline)
			return logline

	def view_log_file(self):
		"""View file log."""
		startfile(self.logFileName)

	def purge_logfiles(self):
		"""Purge old log file."""
		now = time()
		for filename in listdir(self.logPathFile):
			# if os.stat(path.join(self.logPathFile, filename)).st_mtime < now - self.daysDelFile * 86400:
			if path.getmtime(path.join(self.logPathFile, filename)) < now - self.daysDelFile * 86400:
				if path.isfile(path.join(self.logPathFile, filename)):
					qDebug('remove log file : ' + filename)
					remove(path.join(self.logPathFile, filename))