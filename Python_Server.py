from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import string, sys
from twisted.protocols.basic import LineReceiver
from twisted.internet.error import CannotListenError
from twisted.internet.interfaces import IReactorTCP
portNumber = 6789
ipAddress = '131.179.16.191'
numQueues = 2

class Server(LineReceiver):
    delimiter = '\n'

    def __init__(self, factory):

        self.factory = factory
        self.numPlayer = self.factory.connections
        self.factory.players.append(self)


    def connectionMade(self):

        print("Successfully connected with Player " + str(self.numPlayer))
        print("Current Players List: " + str(self.factory.players))

    def connectionLost(self, reason):
        
        self.factory.connections-=1
        self.factory.players.remove(self)
        print("The connection for player: " + str(self.numPlayer) + " was lost. " + str(self.factory.connections) + " are left")

    def lineReceived(self, line):
        print("Line Received from Player " + str(self.numPlayer) + '\n' + line)

class ServerFactory(Factory):

    def __init__(self):

        print("Initiliazing ServerFactory...")
        print("Attemping to create TCP Endpoint for Server with:\n"
        + "Port: " + str(portNumber) + "\nIP Address: " + ipAddress)

        self.players = []
        self.connections = 0

        print("Number of Connections: " + str(self.connections))

    def buildProtocol(self, addr):

        self.connections += 1
        print("Number of Connections: " + str(self.connections))

        return Server(self)


try:

    serverFactory = ServerFactory()
    reactor.listenTCP(portNumber, serverFactory, numQueues, ipAddress)

    print("Successfully created Socket...")

except CannotListenError:
    print("Error creating socket")

reactor.run()
