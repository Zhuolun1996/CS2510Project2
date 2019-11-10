import struct


class SocketMessageManager:
    '''
    Socket message manager
    '''

    @staticmethod
    def sendMessage(sock, msg, statisticHelper):
        # Prefix each message with a 4-byte length (network byte order)
        msg = struct.pack('>I', len(msg)) + msg
        statisticHelper.messageSend += 1
        statisticHelper.bytesSend += len(msg)
        sock.sendall(msg)

    @staticmethod
    def recvMessage(sock, statisticHelper):
        # Read message length
        rawMessageLength = SocketMessageManager.recvAll(sock, 4)
        if not rawMessageLength:
            return None
        messageLength = struct.unpack('>I', rawMessageLength)[0]
        # Read the message data
        msg = SocketMessageManager.recvAll(sock, messageLength)
        statisticHelper.messageRecv += 1
        statisticHelper.bytesRecv += len(msg)
        return msg

    @staticmethod
    def recvAll(sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data
