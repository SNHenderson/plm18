import os

class Logger(object):
    def __init__(self, filename):

        # Makes any necessary directories (i.e, logs/)
        dirname = os.path.dirname(filename)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        self.file = open(filename, 'w')

    def log(self, *args):
        print(*args, file=self.file)

    def close(self):
        self.file.close()
