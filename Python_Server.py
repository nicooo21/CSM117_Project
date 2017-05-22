from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver
import string, sys
from twisted.internet.error import CannotListenError
from twisted.internet.interfaces import IReactorTCP
portNumber = 6789
ipAddress = '127.0.0.1'
numQueues = 2

class Server(LineReceiver):
    
    def __init__(self, factory):

        self.factory = factory
        self.numPlayer = self.factory.connections
        self.factory.players.append(self)


    def connectionMade(self):
        
        print("Successfully connected with Player: " + str(self.numPlayer))
        print("Current Players List: " + str(self.factory.players))


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
