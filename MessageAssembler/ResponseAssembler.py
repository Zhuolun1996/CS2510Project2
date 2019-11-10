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
