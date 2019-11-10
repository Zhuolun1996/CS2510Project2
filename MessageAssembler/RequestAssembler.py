import json


class RequestAssembler:
    '''
    Request assembler
    '''

    @staticmethod
    def assembleConnectRequest():
        request = dict()
        request['head'] = 'connectRequest'
        return json.dumps(request)

    @staticmethod
    def assembleGetFileListFromServerRequest():
        request = dict()
        request['head'] = 'getFileListFromServerRequest'
        return json.dumps(request)

    @staticmethod
    def assembleNewFileRequest(fileName, content):
        request = dict()
        request['head'] = 'newFileRequest'
        request['fileName'] = fileName
        request['content'] = content
        return json.dumps(request)

    @staticmethod
    def assembleJoinNetworkRequest(nodeId, nodeIp, nodePort):
        request = dict()
        request['head'] = 'joinNetworkRequest'
        request['nodeId'] = nodeId
        request['nodeIp'] = nodeIp
        request['nodePort'] = nodePort
        return json.dumps(request)

    @staticmethod
    def assembleAddFileRequest(fileName, content, forward):
        request = dict()
        request['head'] = 'addFileRequest'
        request['fileName'] = fileName
        request['content'] = content
        request['forward'] = forward
        return json.dumps(request)

    @staticmethod
    def assembleReadFileRequest(fileName):
        request = dict()
        request['head'] = 'readFileRequest'
        request['fileName'] = fileName
        return json.dumps(request)

    @staticmethod
    def assembleGetFileListFromNodeRequest():
        request = dict()
        request['head'] = 'getFileListFromNodeRequest'
        return json.dumps(request)
