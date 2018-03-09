import os

class Logger(object):
    def __init__(self, file):

        # Makes any necessary directories (i.e, logs/)
        dirname = os.path.dirname(file)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        self.file_name = file
        self.file = open(file, 'w')

    def print(self, *args):
        print(*args)
        print(*args, file = self.file)

    def close(self):
        self.file.close()