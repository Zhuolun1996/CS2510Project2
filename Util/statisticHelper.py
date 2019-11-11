import time


class statisticHelper:
    def __init__(self):
        self.messageSend = 0
        self.messageRecv = 0
        self.bytesSend = 0
        self.bytesRecv = 0
        self.averageTime = 0

    def computeAverageResponseTime(self, startTime):
        currentTime = time.time() * 1000
        responseTime = currentTime - startTime
        self.averageTime = (self.averageTime * (self.messageSend - 1) + responseTime) / self.messageSend

    def printStatisticData(self):
        print('======= Statistic Data ======')
        print('Message Send: {}'.format(self.messageSend))
        print('Message Recv: {}'.format(self.messageRecv))
        print('Bytes Send: {}'.format(self.bytesSend))
        print('Bytes Recv: {}'.format(self.bytesRecv))
        print('Average Response Time: {}'.format(self.averageTime))