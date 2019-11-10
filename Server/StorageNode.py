import socketserver
import json
import socket
import time
import os
from Util.SocketMessageManager import SocketMessageManager
from Util.statisticHelper import statisticHelper
from Server.Server import Server
from Server.baseClient import baseClient
from MessageAssembler.ResponseAssembler import ResponseAssembler
from MessageAssembler.RequestAssembler import RequestAssembler
from Server.DirectoryServer import DirectoryServer


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
        if requestHead == 'addFileRequest':
            fileName = request['fileName']
            content = request['content']
            forward = request['forward']
            return server.createAddFileResponse(fileName, content, forward)
        elif requestHead == 'readFileRequest':
            fileName = request['fileName']
            return server.createReadFileResponse(fileName)
        elif requestHead == 'getFileListFromNodeRequest':
            return server.assembleGetFileListFromNodeResponse()


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def setup(self, server):
        self.server = server

    def getServer(self):
        return self.server


class StorageNode(Server, baseClient):
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

    def initFilePath(self):
        if not self.getDirectoryPath().parent.exists():
            os.mkdir(self.getDirectoryPath().parent)
        if not self.getDirectoryPath().exists():
            os.mkdir(self.getDirectoryPath())

    def createAddFileResponse(self, fileName, content, forward):
        targetFilePath = self.getDirectoryPath().joinpath(fileName)
        if not targetFilePath.exists():
            with targetFilePath.open('wb') as file:
                file.write(bytes(content, 'utf-8'))
            self.fileList.append(fileName)
        if forward:
            self.sendMessage(DirectoryServer.getDirectoryServerAddress(),
                             RequestAssembler.assembleNewFileRequest(fileName, content))
        return ResponseAssembler.assembleAddFileResponse(True)

    def createReadFileResponse(self, fileName):
        targetFilePath = self.getDirectoryPath().joinpath(fileName)
        if targetFilePath.exists():
            return ResponseAssembler.assembleReadFileResponse(self.getFileContent(fileName))
        else:
            raise Exception('Reading File Not Exists')

    def createGetFileListFromNodeResponse(self):
        return ResponseAssembler.assembleGetFileListFromNodeResponse(self.fileList)

    def requestJoinNetwork(self):
        rawResponse = self.sendMessage(DirectoryServer.getDirectoryServerAddress(),
                                       RequestAssembler.assembleJoinNetworkRequest(self.id, self.address[0],
                                                                                   self.address[1]))
        response = json.loads(rawResponse)
        if response['result'] != True:
            raise Exception('Join Network Error')

    def getFileContent(self, fileName):
        with self.getDirectoryPath().joinpath(fileName).open('r') as file:
            content = file.read()
            return content
