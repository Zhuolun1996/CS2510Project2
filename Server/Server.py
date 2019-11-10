import threading
import socketserver
from pathlib import Path


class Server:
    '''
    Server class
    '''

    def __init__(self, id, name, address, statisticHelper, TCPServer, TCPHandler, output):
        self.id = id
        self.name = name
        self.address = address
        self.statisticHelper = statisticHelper
        self.output = output
        socketserver.TCPServer.allow_reuse_address = True
        self.server = TCPServer(self.address, TCPHandler)
        self.server.setup(self)

    def startServer(self):
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=self.server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        print("Server " + str(self.id) + " loop running in thread:", server_thread.name)

    def shutdownServer(self):
        '''
        Shutdown server
        stop listening
        release resources
        :return:
        '''
        self.server.shutdown()
        self.server.server_close()
        print("Server" + str(self.id) + " shutdown")

    def getServer(self):
        return self.server

    def getAddress(self):
        return self.server.server_address

    def getDirectoryPath(self):
        return Path('./Files/' + str(self.id))
