import socketserver
import json
import socket
import time
import random
from Util.SocketMessageManager import SocketMessageManager
from Util.statisticHelper import statisticHelper
from Server.Server import Server
from Server.baseClient import baseClient
from MessageAssembler.RequestAssembler import RequestAssembler
from MessageAssembler.ResponseAssembler import ResponseAssembler


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    '''
    Handler to process TCP connection
    '''

    def handle(self):
        '''
        Process coming in TCP message and send response
        :return:
        '''
        data = str(SocketMessageManager.recvMessage(self.request, self.server.getServer().statisticHelper), 'utf-8')
        startTime = time.time() * 1000
        if self.server.getServer().output == 'debug':
            print("Server {} Received: {}".format(self.server.getServer().id, data))
        response = self.processRequest(json.loads(data), self.server.getServer())
        self.request.settimeout(0.5)
        try:
            SocketMessageManager.sendMessage(self.request, bytes(response, 'utf-8'),
                                             self.server.getServer().statisticHelper)
            self.server.getServer().statisticHelper.computeAverageResponseTime(startTime)
        except socket.timeout:
            print("Server {} timeout".format(self.request.address))
            print("Request Fault Tolerance Schema")
            raise socket.timeout
        if self.server.getServer().output == 'debug':
            print("Server {} send: {}".format(self.server.getServer().id, response))

    def processRequest(self, request, server):
        '''
        Create response based on the request head
        :param request: request
        :param server: server
        :return:
        '''
        requestHead = request['head']
        if requestHead == 'connectRequest':
            return server.createConnectResponse()
        elif requestHead == 'getFileListFromServerRequest':
            return server.createGetFileListFromServerResponse()
        elif requestHead == 'newFileRequest':
            fileName = request['fileName']
            content = request['content']
            return server.createNewFileResponse(fileName, content)
        elif requestHead == 'joinNetworkRequest':
            nodeId = request['nodeId']
            nodeIp = request['nodeIp']
            nodePort = request['nodePort']
            return server.createJoinNetworkResponse(nodeId, nodeIp, nodePort)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def setup(self, server):
        self.server = server

    def getServer(self):
        return self.server


class DirectoryServer(Server, baseClient):
    def __init__(self, id, name, address, output):
        self.statisticHelper = statisticHelper()
        Server.__init__(self, id, name, address, self.statisticHelper, ThreadedTCPServer, ThreadedTCPRequestHandler,
                        output)
        baseClient.__init__(self, id, name, address, self.statisticHelper, output)
        self.nodeList = list()
        self.fileList = list()

    def setNodeList(self, nodeList):
        self.nodeList = nodeList

    def setFileList(self, fileList):
        self.fileList = fileList

    def createConnectResponse(self):
        nodeId, address = random.choice(self.nodeList)
        return ResponseAssembler.assembleConnectResponse(nodeId, address[0], address[1])

    def createGetFileListFromServerResponse(self):
        return ResponseAssembler.assembleGetFileListFromServerResponse(self.fileList)

    def createNewFileResponse(self, fileName, content):
        self.fileList.append(fileName)
        for nodeId, address in self.nodeList:
            self.sendMessage(address, RequestAssembler.assembleAddFileRequest(fileName, content, False))
        return ResponseAssembler.assembleNewFileResponse(True)

    def createJoinNetworkResponse(self, nodeId, nodeIp, nodePort):
        self.nodeList.append((nodeId, (nodeIp, nodePort)))
        return ResponseAssembler.assembleJoinNetworkResponse(True)
