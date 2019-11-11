import socketserver
import json
import socket
import time
import random
import copy
from Util.SocketMessageManager import SocketMessageManager
from Util.statisticHelper import statisticHelper
from Server.Server import Server
from Server.baseClient import baseClient
from MessageAssembler.RequestAssembler import RequestAssembler
from MessageAssembler.ResponseAssembler import ResponseAssembler
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
        elif requestHead == 'joinBackupListRequest':
            serverId = request['serverId']
            serverIp = request['serverIp']
            serverPort = request['serverPort']
            return server.createJoinBackupListResponse(serverId, serverIp, serverPort)
        elif requestHead == 'getBackupServerRequest':
            return server.createGetBackupServerResponse()
        elif requestHead == 'copyServerRequest':
            nodeList = request['nodeList']
            fileList = request['fileList']
            backupServerList = request['backupServerList']
            return server.createCopyServerResponse(nodeList, fileList, backupServerList)
        elif requestHead == 'cloneServerRequest':
            serverId = request['serverId']
            return server.createCloneServerResponse(serverId)
        elif requestHead == 'cloneNodeRequest':
            return server.createCloneNodeResponse(json.dumps(request))
        elif requestHead == 'storageNodeRemoveRequest':
            nodeId = request['nodeId']
            return server.createRemoveNodeResponse(nodeId)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def setup(self, server):
        self.server = server

    def getServer(self):
        return self.server


class DirectoryServer(Server, baseClient):
    def __init__(self, id, name, address, cachedDirectoryServerAddress, output):
        self.statisticHelper = statisticHelper()
        self.id = id
        Server.__init__(self, id, name, address, self.statisticHelper, ThreadedTCPServer, ThreadedTCPRequestHandler,
                        output)
        baseClient.__init__(self, id, name, address, self.statisticHelper, output)
        self.nodeList = list()
        self.fileList = list()
        self.backupServerList = list()
        self.cachedDirectoryServerAddress = cachedDirectoryServerAddress

    def setNodeList(self, nodeList):
        self.nodeList = nodeList

    def setFileList(self, fileList):
        self.fileList = fileList

    def setBackupList(self, backupList):
        self.backupServerList = backupList

    def createConnectResponse(self):
        nodeId, address = random.choice(self.nodeList)
        return ResponseAssembler.assembleConnectResponse(nodeId, address[0], address[1])

    def createGetFileListFromServerResponse(self):
        return ResponseAssembler.assembleGetFileListFromServerResponse(self.fileList)

    def createNewFileResponse(self, fileName, content):
        if fileName not in self.fileList:
            self.fileList.append(fileName)
            for nodeId, address in self.nodeList:
                self.sendMessage(tuple(address), RequestAssembler.assembleAddFileRequest(fileName, content, False))
            for serverId, address in self.backupServerList:
                try:
                    self.requestCopyServer(address)
                except:
                    print('wait for recovery')
            return ResponseAssembler.assembleNewFileResponse(True)
        else:
            return ResponseAssembler.assembleNewFileResponse(False)


    def createJoinNetworkResponse(self, nodeId, nodeIp, nodePort):
        self.nodeList.append([nodeId, [nodeIp, nodePort]])
        for serverId, address in self.backupServerList:
            try:
                self.requestCopyServer(address)
            except:
                print('wait for recovery')
        return ResponseAssembler.assembleJoinNetworkResponse(True)

    def createJoinBackupListResponse(self, serverId, serverIp, serverPort):
        self.backupServerList.append([serverId, [serverIp, serverPort]])
        for serverId, address in self.backupServerList:
            try:
                self.requestCopyServer(address)
            except:
                print('wait for recovery')
        return ResponseAssembler.assembleJoinBackupListResponse(True)

    def createGetBackupServerResponse(self):
        if len(self.backupServerList) > 0:
            serverId, (serverIp, serverPort) = self.backupServerList[0]
            return ResponseAssembler.assembleGetBackupServerResponse(serverId, serverIp, serverPort)
        else:
            raise Exception('No Backup Server')

    def createCopyServerResponse(self, nodeList, fileList, backupServerList):
        self.setNodeList(nodeList)
        self.setFileList(fileList)
        self.setBackupList(backupServerList)
        return ResponseAssembler.assembleCopyServerResponse(True)

    def createCloneServerResponse(self, serverId):
        nodeList = self.nodeList
        fileList = self.fileList
        backupList = copy.deepcopy(self.backupServerList)
        backupList.append([self.id, list(self.address)])
        for i in range(len(backupList)):
            if backupList[i][0] == serverId:
                backupList.pop(i)
                break
        return ResponseAssembler.assembleCloneServerResponse(nodeList, fileList, backupList)

    def requestJoinBackupList(self, serverId, serverIp, serverPort):
        self.sendMessage(self.cachedDirectoryServerAddress,
                         RequestAssembler.assembleJoinBackupListRequest(serverId, serverIp, serverPort))

    def requestCloneServer(self, targetAddress):
        return self.sendMessage(tuple(targetAddress), RequestAssembler.assembleCloneServerRequest(self.id))

    def requestCopyServer(self, targetAddress):
        return self.sendMessage(tuple(targetAddress), RequestAssembler.assembleCopyServerRequest(self.nodeList, self.fileList,
                                                                                          self.backupServerList))

    def joinBackupList(self, serverId, serverIp, serverPort):
        self.requestJoinBackupList(serverId, serverIp, serverPort)
        self.cloneServer(self.cachedDirectoryServerAddress)

    def createCloneNodeResponse(self, request):
        if len(self.nodeList) > 0:
            node = self.nodeList[0]
            while True:
                try:
                    response = self.sendMessage(tuple(node[1]), request)
                    break
                except:
                    self.nodeList.remove(node)
                    node = random.choice(self.nodeList)
            return response
        return ResponseAssembler.assembleErrorResponse('First Node Join')

    def cloneServer(self, address):
        rawResponse = self.requestCloneServer(address)
        response = json.loads(rawResponse)
        nodeList = response['nodeList']
        fileList = response['fileList']
        backupList = response['backupServerList']
        self.nodeList = nodeList
        self.fileList = fileList
        self.backupServerList = backupList

    def createRemoveNodeResponse(self, nodeId):
        for i in range(len(self.nodeList)):
            if self.nodeList[i][0] == int(nodeId):
                self.nodeList.pop(i)
                break
        for serverId, address in self.backupServerList:
            try:
                self.requestCopyServer(address)
            except:
                print('wait for recovery')
        return ResponseAssembler.assembleStorageNodeRemoveResponse(True)