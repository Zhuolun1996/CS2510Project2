import socket
import time
from Util.SocketMessageManager import SocketMessageManager


class baseClient:
    '''
    Client class
    '''

    def __init__(self, id, name, address, statisticHelper, output):
        self.id = id
        self.name = name
        self.address = address
        self.statisticHelper = statisticHelper
        self.output = output

    def sendMessage(self, address, message):
        '''
        Send message and listening for the response
        :param address: address
        :param message: message
        :return: response
        '''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(address)
            try:
                SocketMessageManager.sendMessage(sock, bytes(message, 'utf-8'), self.statisticHelper)
                startTime = time.time() * 1000
            except:
                raise Exception('sent message fail')
            if self.output == 'debug':
                print("Client {} send: {} to {}".format(self.id, message, str(address)))
            sock.settimeout(0.5)
            try:
                response = str(SocketMessageManager.recvMessage(sock, self.statisticHelper),
                               'utf-8')
                self.statisticHelper.computeAverageResponseTime(startTime)
            except socket.timeout:
                print("Server {} timeout".format(address))
                print("Request Fault Tolerance Schema")
                raise socket.timeout
            if self.output == 'debug':
                print("Client {} Received: {}".format(self.id, response))
            return response
