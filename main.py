import argparse
import time
from Server.DirectoryServer import DirectoryServer
from Server.StorageNode import StorageNode
from Server.Client import Client
from Util.statisticHelper import statisticHelper
import traceback
from Util.readFileThread import readFileThread

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-C', '--clients', help='Number of clients', type=int, required=True)
    parser.add_argument('-B', '--backups', help='Number of clients', type=int, required=True)
    parser.add_argument('-S', '--nodes', help='Number of storage nodes', type=int, required=True)
    parser.add_argument('-M', '--files', help='Number of Files', type=int, required=True)
    parser.add_argument('-N', '--requests', help='Number of Requests', type=int, required=True)
    parser.add_argument('-F', '--frequency', help='Request Frequency', type=float, required=True)
    parser.add_argument('-L', '--length', help='File Length', type=int, required=True)
    parser.add_argument('-O', '--output', help='enable message output: clean || debug || false', type=str,
                        required=True)
    args = parser.parse_args()

    CLIENTS = args.clients
    BACKUPS = args.backups
    NODES = args.nodes
    FILES = args.files
    REQUESTS = args.requests
    FREQUENCY = args.frequency
    LENGTH = args.length
    OUTPUT = args.output

    clientList = list()
    nodeList = list()
    backupList = list()
    try:
        # init Directory Server
        primaryDirectoryServer = DirectoryServer(10000, 'DirectoryServer', ('127.0.0.1', 50100),
                                                 ('127.0.0.1', 50100), OUTPUT)
        primaryDirectoryServer.startServer()

        for i in range(BACKUPS):
            backupList.append(
                DirectoryServer(10001 + i, 'DirectoryServer', ('127.0.0.1', 50101 + i),
                                primaryDirectoryServer.getAddress(), OUTPUT))

        for backupServer in backupList:
            backupServer.startServer()
            backupServer.joinBackupList(backupServer.id, backupServer.address[0], backupServer.address[1])

        # init Storage Nodes
        for i in range(NODES):
            nodeList.append(
                StorageNode(100 + i, 'storageNode' + str(i), ('127.0.0.1', 50200 + i),
                            primaryDirectoryServer.getAddress(), OUTPUT))

        for node in nodeList:
            node.startServer()
            node.setup()

        # init clients
        for i in range(0, CLIENTS):
            clientList.append(
                Client(i, 'client' + str(i), ('127.0.0.1', 50000 + i), statisticHelper(),
                       primaryDirectoryServer.getAddress(), OUTPUT))

        for client in clientList:
            client.setup(FILES, LENGTH)

        primaryDirectoryServer.shutdownServer()

        # test add file
        for i in range(0, FILES):
            clientList[0].requestAddFile(str(i), clientList[0].getFileContent(str(i)))
            time.sleep(1 / FREQUENCY)

        primaryDirectoryServer = DirectoryServer(10000, 'DirectoryServer', ('127.0.0.1', 50100),
                                                 ('127.0.0.1', 50100), OUTPUT)
        primaryDirectoryServer.startServer()

        primaryDirectoryServer.cloneServer(backupList[0].getAddress())

        # test add file
        for i in range(0, FILES):
            clientList[0].requestAddFile(str(i), clientList[0].getFileContent(str(i)))
            time.sleep(1 / FREQUENCY)



        # test get file list from server
        clientList[0].requestGetFileListFromServer()

        # test get file list from node
        clientList[0].requestGetFileListFromNode()

        # test sequential read file
        for i in range(REQUESTS):
            clientList[0].requestReadFile(str(int(i % FILES)))
            time.sleep(1 / FREQUENCY)

        for i in range(NODES - 1):
            nodeList[i].shutdownServer()

        # test sequential read file
        for i in range(REQUESTS):
            clientList[0].requestReadFile(str(int(i % FILES)))
            time.sleep(1 / FREQUENCY)

        for i in range(NODES - 1):
            nodeList[i] = StorageNode(100 + i, 'storageNode' + str(i), ('127.0.0.1', 50200 + i),
                                      primaryDirectoryServer.getAddress(), OUTPUT)
            nodeList[i].startServer()
            nodeList[i].setup()

        # test sequential read file
        for i in range(REQUESTS):
            clientList[0].requestReadFile(str(int(i % FILES)))
            time.sleep(1 / FREQUENCY)


        # test concurrent read file
        readThreads = list()
        for i in range(CLIENTS):
            readThreads.append(readFileThread(clientList[0], str(int(i % FILES)), REQUESTS, FREQUENCY))
        for readThread in readThreads:
            readThread.run()

    except Exception:
        traceback.print_exc()

    finally:
        primaryDirectoryServer.shutdownServer()
        primaryDirectoryServer.statisticHelper.printStatisticData(primaryDirectoryServer.address[1])
        for backupServer in backupList:
            backupServer.statisticHelper.printStatisticData(backupServer.address[1])
            backupServer.shutdownServer()
        for node in nodeList:
            node.statisticHelper.printStatisticData(node.address[1])
            node.shutdownServer()
        for client in clientList:
            client.statisticHelper.printStatisticData(client.address[1])


if __name__ == "__main__":
    main()
