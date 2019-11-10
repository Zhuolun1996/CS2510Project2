import os
import json
from MessageAssembler.RequestAssembler import RequestAssembler
import shutil
from pathlib import Path
from Server.baseClient import baseClient
import socket


class Client(baseClient):
    '''
    Client class
    '''

    def __init__(self, id, name, address, statisticHelper, primaryServer, backupServer, output):
        baseClient.__init__(self, id, name, address, statisticHelper, output)
        self.cachedNodeId = None
        self.cachedNodeAddress = None
        self.cachedDirectoryServer = primaryServer
        self.backupDirectoryServer = backupServer

    def switchBackupServer(self):
        temp = self.cachedDirectoryServer
        self.cachedDirectoryServer = self.backupDirectoryServer
        self.backupDirectoryServer = temp

    def setUp(self, FILE, LENGTH):
        self.cleanFileDirectory()
        self.initFiles(FILE, LENGTH)
        return self.requestConnect()

    def getDirectoryPath(self):
        return Path('./Files/' + str(self.id))

    def initFiles(self, num, length):
        '''
        Create files for peers (for test only)
        :param num: number of files
        :param length: each file length
        :return:
        '''
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
        try:
            rawResponse = self.sendMessage(self.cachedDirectoryServer.getAddress(),
                                           RequestAssembler.assembleConnectRequest())
            response = json.loads(rawResponse)
            self.cachedNodeId = response['nodeId']
            self.cachedNodeAddress = (response['nodeIp'], response['nodePort'])
        except socket.timeout:
            self.switchBackupServer()
            self.requestConnect()

    def requestGetFileListFromServer(self):
        try:
            rawResponse = self.sendMessage(self.cachedDirectoryServer.getAddress(),
                                           RequestAssembler.assembleGetFileListFromServerRequest())
            response = json.loads(rawResponse)
            print('=== Get File List From Directory Server ===\nFile List: {}'.format(response['fileList']))
        except socket.timeout:
            self.switchBackupServer()
            self.requestGetFileListFromServer()

    def requestNewFile(self, fileName, content):
        try:
            self.sendMessage(self.cachedDirectoryServer.getAddress(),
                             RequestAssembler.assembleNewFileRequest(fileName, content))
        except socket.timeout:
            self.switchBackupServer()
            self.requestGetFileListFromServer()

    def requestAddFile(self, fileName, content):
        if self.cachedNodeAddress != None:
            self.sendMessage(self.cachedNodeAddress, RequestAssembler.assembleAddFileRequest(fileName, content, True))
        else:
            raise Exception('Need Connect To Directory Server First')

    def requestReadFile(self, fileName):
        if self.cachedNodeAddress != None:
            rawResponse = self.sendMessage(self.cachedNodeAddress, RequestAssembler.assembleReadFileRequest(fileName))
            response = json.loads(rawResponse)
            print('=== Read File ===\nFile Name: {}\nContent: {}'.format(fileName, response['content']))
        else:
            raise Exception('Need Connect To Directory Server First')

    def requestGetFileListFromNode(self):
        if self.cachedNodeAddress != None:
            rawResponse = self.sendMessage(self.cachedNodeAddress,
                                           RequestAssembler.assembleGetFileListFromServerRequest())
            response = json.loads(rawResponse)
            print('=== Get File List From Node ===\nFile List: {}'.format(response['fileList']))
        else:
            raise Exception('Need Connect To Directory Server First')

    def getFileContent(self, fileName):
        with self.getDirectoryPath().joinpath(fileName).open('r') as file:
            content = file.read()
            return content
