from threading import Thread


class readFileThread(Thread):
    def __init__(self, client, fileName):
        Thread.__init__(self)
        self.client = client
        self.fileName = fileName

    def run(self):
        self.client.requestReadFile(self.fileName)
