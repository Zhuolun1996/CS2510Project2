import argparse
import time
from Server.DirectoryServer import DirectoryServer
from Server.StorageNode import StorageNode
from Server.Client import Client
from Util.statisticHelper import statisticHelper
import random
import traceback
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-C', '--clients', help='Number of clients', type=int, required=True)
    parser.add_argument('-S', '--nodes', help='Number of storage nodes', type=int, required=True)
    parser.add_argument('-M', '--files', help='Number of Files', type=int, required=True)
    parser.add_argument('-N', '--requests', help='Number of Requests', type=int, required=True)
    parser.add_argument('-F', '--frequency', help='Request Frequency', type=float, required=True)
    parser.add_argument('-L', '--length', help='File Length', type=int, required=True)
    parser.add_argument('-O', '--output', help='enable message output: clean || debug || false', type=str,
                        required=True)
    args = parser.parse_args()

    CLIENTS = args.clients
    NODES = args.nodes
    FILES = args.files
    REQUESTS = args.requests
    FREQUENCY = args.frequency
    LENGTH = args.length
    OUTPUT = args.output

    clientList = list()
    nodeList = list()
    try:
        # init Directory Server
        directroyServer = DirectoryServer(10000, 'DirectoryServer', ('127.0.0.1', 50100), OUTPUT)
        directroyServer.startServer()

        # init Storage Nodes
        for i in range(0, NODES):
            nodeList.append(StorageNode(100 + i, 'storageNode' + str(i), ('127.0.0.1', 50101 + i), OUTPUT))

        for node in nodeList:
            node.startServer()
            node.initFilePath()
            node.requestJoinNetwork()

        # init clients
        for i in range(0, CLIENTS):
            clientList.append(
                Client(i, 'client' + str(i), ('127.0.0.1', 50000 + i), statisticHelper(), OUTPUT))

        for client in clientList:
            client.setUp(FILES, LENGTH)

        # test add file
        for i in range(0, FILES):
            clientList[0].requestAddFile(str(i), clientList[0].getFileContent(str(i)))
            time.sleep(1 / FREQUENCY)

        # test sequential read file
        for i in range(REQUESTS):
            clientList[0].requestReadFile(str(random.randint(0, FILES - 1)))
            time.sleep(1 / FREQUENCY)
    except Exception:
        traceback.print_exc()

    finally:
        directroyServer.shutdownServer()
        for node in nodeList:
            node.shutdownServer()


if __name__ == "__main__":
    main()
