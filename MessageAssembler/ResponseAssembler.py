import json


class ResponseAssembler:
    '''
    Request assembler
    '''

    @staticmethod
    def assembleConnectResponse(nodeId, nodeIp, nodePort):
        response = dict()
        response['head'] = 'connectResponse'
        response['nodeId'] = nodeId
        response['nodeIp'] = nodeIp
        response['nodePort'] = nodePort
        return json.dumps(response)

    @staticmethod
    def assembleGetFileListFromServerResponse(fileList):
        response = dict()
        response['head'] = 'getFileListFromServerResponse'
        response['fileList'] = fileList
        return json.dumps(response)

    @staticmethod
    def assembleNewFileResponse(result):
        response = dict()
        response['head'] = 'newFileResponse'
        response['result'] = result
        return json.dumps(response)

    @staticmethod
    def assembleJoinNetworkResponse(result):
        response = dict()
        response['head'] = 'joinNetworkResponse'
        response['result'] = result
        return json.dumps(response)

    @staticmethod
    def assembleAddFileResponse(result):
        response = dict()
        response['head'] = 'addFileResponse'
        response['result'] = result
        return json.dumps(response)

    @staticmethod
    def assembleReadFileResponse(content):
        response = dict()
        response['head'] = 'readFileResponse'
        response['content'] = content
        return json.dumps(response)

    @staticmethod
    def assembleGetFileListFromNodeResponse(fileList):
        response = dict()
        response['head'] = 'getFileListFromNodeResponse'
        response['fileList'] = fileList
        return json.dumps(response)

    @staticmethod
    def assembleCloneNodeResponse(fileDict, cachedDirectoryServer, backupDirectoryServer):
        response = dict()
        response['head'] = 'copyNodeResponse'
        response['fileDict'] = fileDict
        response['cachedDirectoryServer'] = cachedDirectoryServer
        response['backupDirectoryServer'] = backupDirectoryServer
        return json.dumps(response)

    @staticmethod
    def assembleCopyServerResponse(result):
        response = dict()
        response['head'] = 'copyServerResponse'
        response['result'] = result
        return json.dumps(response)

    @staticmethod
    def assembleCloneServerResponse(nodeList, fileList, backupServerList):
        response = dict()
        response['head'] = 'cloneServerResponse'
        response['nodeList'] = nodeList
        response['fileList'] = fileList
        response['backupServerList'] = backupServerList
        return json.dumps(response)

    @staticmethod
    def assembleJoinBackupListResponse(result):
        response = dict()
        response['head'] = 'joinBackupListResponse'
        response['result'] = result
        return json.dumps(response)

    @staticmethod
    def assembleGetBackupServerResponse(serverId, serverIp, serverPort):
        response = dict()
        response['head'] = 'getBackupServerResponse'
        response['serverId'] = serverId
        response['serverIp'] = serverIp
        response['serverPort'] = serverPort
        return json.dumps(response)

    @staticmethod
    def assembleStorageNodeRemoveResponse(result):
        response = dict()
        response['head'] = 'storageNodeRemoveResponse'
        response['result'] = result
        return json.dumps(response)

    @staticmethod
    def assembleErrorResponse(errorBody):
        response = dict()
        response['head'] = 'errorResponse'
        response['error'] = errorBody
        return json.dumps(response)