from threading import Thread
import time

class readFileThread(Thread):
    def __init__(self, client, fileName, R, F):
        Thread.__init__(self)
        self.client = client
        self.fileName = fileName
        self.R = R
        self.F = F

    def run(self):
        for i in range(self.R):
            self.client.requestReadFile(self.fileName)
            time.sleep(1 / self.F)
