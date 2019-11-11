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
from Exception.ServerError import ServerError


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    '''
    Handler to process TCP connection
    '''

    def handle(self):
        '''
        Process coming in TCP message and send response
        :return:
        '''
        try:
            data = str(SocketMessageManager.recvMessage(self.request, self.server.getServer().statisticHelper), 'utf-8')
            startTime = time.time() * 1000
            if self.server.getServer().output == 'debug':
                print("Server {} Received: {}".format(self.server.getServer().id, data))
            response = self.processRequest(json.loads(data), self.server.getServer())
            self.request.settimeout(0.5)
            SocketMessageManager.sendMessage(self.request, bytes(response, 'utf-8'),
                                             self.server.getServer().statisticHelper)
            self.server.getServer().statisticHelper.computeAverageResponseTime(startTime)
        except (socket.timeout, ConnectionRefusedError):
            print("Server {} timeout".format(self.request.address))
            print("Request Fault Tolerance Schema")
            raise ServerError('Server Error')
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
            return server.createGetFileListFromNodeResponse()
        elif requestHead == 'cloneNodeRequest':
            return server.createCloneNodeResponse()


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def setup(self, server):
        self.server = server

    def getServer(self):
        return self.server


class StorageNode(Server, baseClient):
    def __init__(self, id, name, address, primaryServerAddress, output):
        self.statisticHelper = statisticHelper()
        Server.__init__(self, id, name, address, self.statisticHelper, ThreadedTCPServer, ThreadedTCPRequestHandler,
                        output)
        baseClient.__init__(self, id, name, address, self.statisticHelper, output)
        self.cachedDirectoryServerAddress = primaryServerAddress
        self.backupDirectoryServerAddress = None
        self.fileList = list()

    def setFileList(self, fileList):
        self.fileList = fileList

    def setup(self):
        self.cleanFileDirectory()
        self.initFilePath()
        self.requestJoinNetwork()
        self.getBackupServer()
        self.requestCloneNode()


    def switchBackupServer(self):
        self.cachedDirectoryServerAddress = self.backupDirectoryServerAddress
        self.backupDirectoryServerAddress = self.getBackupServer()

    def createAddFileResponse(self, fileName, content, forward):
        targetFilePath = self.getDirectoryPath().joinpath(fileName)
        if not targetFilePath.exists() and fileName not in self.fileList:
            with targetFilePath.open('wb') as file:
                file.write(bytes(content, 'utf-8'))
            self.fileList.append(fileName)
        if forward:
            while True:
                try:
                    self.sendMessage(self.cachedDirectoryServerAddress,
                                     RequestAssembler.assembleNewFileRequest(fileName, content))
                    break
                except ServerError:
                    self.switchBackupServer()
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
        while True:
            try:
                rawResponse = self.sendMessage(self.cachedDirectoryServerAddress,
                                               RequestAssembler.assembleJoinNetworkRequest(self.id, self.address[0],
                                                                                           self.address[1]))
                break
            except ServerError:
                self.switchBackupServer()
        response = json.loads(rawResponse)
        if response['result'] != True:
            raise Exception('Join Network Error')

    def getFileContent(self, fileName):
        with self.getDirectoryPath().joinpath(fileName).open('r') as file:
            content = file.read()
            return content

    def requestGetBackupServer(self):
        while True:
            try:
                return self.sendMessage(self.cachedDirectoryServerAddress,
                                        RequestAssembler.assembleGetBackupServerRequest())
            except ServerError:
                self.switchBackupServer()

    def getBackupServer(self):
        rawResponse = self.requestGetBackupServer()
        response = json.loads(rawResponse)
        self.backupDirectoryServerAddress = (response['serverIp'], response['serverPort'])

    def requestCloneNode(self):
        rawResponse = self.sendMessage(self.cachedDirectoryServerAddress, RequestAssembler.assembleCloneNodeRequest())
        response = json.loads(rawResponse)
        fileDict = response['fileDict']
        cachedDirectoryServer = response['cachedDirectoryServer']
        backupDirectoryServer = response['backupDirectoryServer']
        self.fileList = list(fileDict.keys())
        self.cachedDirectoryServerAddress = tuple(cachedDirectoryServer)
        self.backupDirectoryServerAddress = tuple(backupDirectoryServer)
        for fileName in self.fileList:
            with self.getDirectoryPath().joinpath(fileName).open('wb') as file:
                file.write(bytes(fileDict[fileName], 'utf-8'))

    def createCloneNodeResponse(self):
        fileDict = dict()
        for fileName in self.fileList:
            content = self.getFileContent(fileName)
            fileDict[fileName] = content
        return ResponseAssembler.assembleCloneNodeResponse(fileDict, self.cachedDirectoryServerAddress,
                                                           self.backupDirectoryServerAddress)
