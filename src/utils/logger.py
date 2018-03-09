class Logger(object):
	def __init__(self, file):
		self.file_name = file
		self.file = open(file, 'w')

	def print(self, *args):
		print(*args)
		print(*args, file = self.file)

	def close(self):
		self.file.close()