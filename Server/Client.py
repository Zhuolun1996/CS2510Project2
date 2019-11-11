import os
import json
from MessageAssembler.RequestAssembler import RequestAssembler
import shutil
from pathlib import Path
from Server.baseClient import baseClient
from Exception.ServerError import ServerError


class Client(baseClient):
    '''
    Client class
    '''

    def __init__(self, id, name, address, statisticHelper, primaryServerAddress, output):
        baseClient.__init__(self, id, name, address, statisticHelper, output)
        self.cachedNodeId = None
        self.cachedNodeAddress = None
        self.cachedDirectoryServerAddress = primaryServerAddress
        self.backupDirectoryServerAddress = None

    def switchBackupServer(self):
        '''
        Switch current cached server to backup server,
        and request for a new backup server.
        :return:
        '''
        self.cachedDirectoryServerAddress = self.backupDirectoryServerAddress
        self.backupDirectoryServerAddress = self.getBackupServer()

    def setup(self, FILE, LENGTH):
        self.cleanFileDirectory()
        self.initFiles(FILE, LENGTH)
        self.requestConnect()
        self.getBackupServer()

    def getDirectoryPath(self):
        return Path('./Files/' + str(self.id))

    def initFiles(self, num, length):
        if not self.getDirectoryPath().parent.exists():
            os.mkdir(self.getDirectoryPath().parent)
        for i in range(0, num):
            if not self.getDirectoryPath().exists():
                os.mkdir(self.getDirectoryPath())
            with self.getDirectoryPath().joinpath(str(i)).open('wb') as file:
                file.write(bytes(('Test File' + str(i)) * length, 'utf-8'))

    def cleanFileDirectory(self):
        '''
        Clean file directory
        :return:
        '''
        try:
            shutil.rmtree(self.getDirectoryPath())
            print('clean directory success')
        except:
            print('clean directory fail')

    def requestConnect(self):
        '''
        Request a storage node and cache this node.
        :return:
        '''
        try:
            rawResponse = self.sendMessage(self.cachedDirectoryServerAddress,
                                           RequestAssembler.assembleConnectRequest())
            response = json.loads(rawResponse)
            self.cachedNodeId = response['nodeId']
            self.cachedNodeAddress = (response['nodeIp'], response['nodePort'])
        except ServerError:
            self.switchBackupServer()
            self.requestConnect()

    def requestGetFileListFromServer(self):
        try:
            rawResponse = self.sendMessage(self.cachedDirectoryServerAddress,
                                           RequestAssembler.assembleGetFileListFromServerRequest())
            response = json.loads(rawResponse)
            if self.output != 'false':
                print('=== Get File List From Directory Server ===\nFile List: {}'.format(response['fileList']))
        except ServerError:
            self.switchBackupServer()
            self.requestGetFileListFromServer()

    def requestNewFile(self, fileName, content):
        try:
            return self.sendMessage(self.cachedDirectoryServerAddress,
                                    RequestAssembler.assembleNewFileRequest(fileName, content))
        except ServerError:
            self.switchBackupServer()
            self.requestNewFile(fileName, content)

    def requestAddFile(self, fileName, content):
        if self.cachedNodeAddress != None:
            while True:
                try:
                    return self.sendMessage(self.cachedNodeAddress,
                                            RequestAssembler.assembleAddFileRequest(fileName, content, True))
                except ServerError:
                    self.requestRemoveNode(self.cachedNodeId)
                    self.requestConnect()
        else:
            raise Exception('Need Connect To Directory Server First')

    def requestReadFile(self, fileName):
        if self.cachedNodeAddress != None:
            while True:
                try:
                    rawResponse = self.sendMessage(self.cachedNodeAddress,
                                                   RequestAssembler.assembleReadFileRequest(fileName))
                    response = json.loads(rawResponse)
                    if self.output != 'false':
                        print('=== Read File ===\nFile Name: {}\nContent: {}'.format(fileName, response['content']))
                    break
                except ServerError:
                    self.requestRemoveNode(self.cachedNodeId)
                    self.requestConnect()
        else:
            raise Exception('Need Connect To Directory Server First')

    def requestGetFileListFromNode(self):
        if self.cachedNodeAddress != None:
            while True:
                try:
                    rawResponse = self.sendMessage(self.cachedNodeAddress,
                                                   RequestAssembler.assembleGetFileListFromNodeRequest())
                    response = json.loads(rawResponse)
                    if self.output != 'false':
                        print('=== Get File List From Node ===\nFile List: {}'.format(response['fileList']))
                    break
                except ServerError:
                    self.requestRemoveNode(self.cachedNodeId)
                    self.requestConnect()
        else:
            raise Exception('Need Connect To Directory Server First')

    def getFileContent(self, fileName):
        with self.getDirectoryPath().joinpath(fileName).open('r') as file:
            content = file.read()
            return content

    def requestGetBackupServer(self):
        return self.sendMessage(self.cachedDirectoryServerAddress,
                                RequestAssembler.assembleGetBackupServerRequest())

    def getBackupServer(self):
        rawResponse = self.requestGetBackupServer()
        response = json.loads(rawResponse)
        self.backupDirectoryServerAddress = (response['serverIp'], response['serverPort'])

    def requestRemoveNode(self, nodeId):
        '''
        Remove a node from the node list
        :param nodeId:
        :return:
        '''
        try:
            return self.sendMessage(self.cachedDirectoryServerAddress,
                                    RequestAssembler.assembleStorageNodeRemoveRequest(str(nodeId)))
        except ServerError:
            self.switchBackupServer()
            self.requestRemoveNode(nodeId)
