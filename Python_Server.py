from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import string, sys
from twisted.protocols.basic import LineReceiver
from twisted.internet.error import CannotListenError
from twisted.internet.interfaces import IReactorTCP
from random import randint

# TCP Connection Information
portNumber = 6789
ipAddress = '127.0.0.1'
numQueues = 2

# Initialization Variables
gridAmount = 2
switchAmount = 2
sliderAmount = 2
switchPressAmount = 2
pressAmount = 1 
switchVSliderAmount = 2
switchVSliderPressAmount = 3
numOptions = 3

# Array Raw and Combinations
switchOptions = ['t', 's']
sliderOptions = ['h', 'v']
horizontalSlider = 'h'
verticalSlider = 'v'
pressOptions = 'f'
totalOptions = [switchOptions, sliderOptions, pressOptions]
switchVSlider = [switchOptions, verticalSlider]
switchPress = [switchOptions, pressOptions]

"""
### Grid Selections ###

# Initialization Notation #
# "type:name?type:name..."

# Two Grid Options


# Grid 0
# Button 0 - Switch or Press
# Button 1 - Horizontal Slider Only
# Button 2 - Anything
# Button 3 - Switch or Vertical Slider

# Grid 1
# Button 0 - Horizontal Slider Only
# Button 1 - Vertical Slider or Switch
# Button 2 - Switch Only
# Button 3 - Press Only

# Switch Names


### Button Options ###

# Switch # - 0
# 0 - Toggle - 't'
# 1 - Switch - 's'

# Slider # - 1
# 0 - Horizontal - 'h'
# 1 - Vertical - 'v'

# Press # - 2 
# 0 - Flat - 'f'
"""


class Server(LineReceiver):

    def __init__(self, factory):

        self.factory = factory
        self.numPlayer = self.factory.connections
        self.factory.players.append(self)
        self.delimiter = '\n'

        # Name Combinations
        self.switchNames = ['a', 'b', 'c', 'd', 'e', 'f']
        self.sliderNames = ['a', 'b', 'c', 'd', 'e', 'f']
        self.pressNames = ['a', 'b', 'c', 'd', 'e', 'f']
        self.optionNames = [self.switchNames, self.sliderNames, self.pressNames]
        self.switchVSliderNames = [self.switchNames, self.sliderNames]
        self.switchPressNames = [self.switchNames, self.pressNames]



    def randomNumber(self, length):
        return randint(0, length - 1)

    def randomNameChar(self, names):
        nameChar = names[self.randomNumber(len(names))]
        print('char: ' + nameChar)
        names.remove(nameChar)
        print("list is now: " + str(names))
        return nameChar


    def initializeGrid(self):
        # Randomize Grid (Either one or zero)
        self.gridNumber = self.randomNumber(gridAmount)
        print ("Grid Layout: " + str(self.gridNumber) + " For Player " + str(self.numPlayer))

        # Randomize Buttons Depending on Grid
        # Grid 1 Layout
        if not self.gridNumber:
            # Initialize Button 0 - Switch or Press + Name

            randNum = self.randomNumber(switchPressAmount)
            buttonOption = switchPress[randNum]

            initializationString = (buttonOption[self.randomNumber(len(buttonOption))]
            + ':' + self.randomNameChar(self.switchPressNames[randNum]) + '?')
            print(initializationString)

            # Initialize Button 1 - Horizontal Slider + Name

            initializationString += horizontalSlider + ':' + self.randomNameChar(self.sliderNames) + '?'
            print(initializationString)

            # Initialize Button 2 - Anything + Name
            randNum = self.randomNumber(numOptions)
            buttonOption = totalOptions[randNum]
            initializationString += (buttonOption[self.randomNumber(len(buttonOption))]
            + ':' + self.randomNameChar(self.optionNames[randNum]) + '?')
            print (initializationString)

            # Initialize Button 3 - Switch or Vertical Slider

            randNum = self.randomNumber(switchVSliderAmount)
            buttonOption = switchVSlider[randNum]
            initializationString += (buttonOption[self.randomNumber(len(buttonOption))]
            + ':' + self.randomNameChar(self.switchVSliderNames[randNum]))

            print("Final String for Grid 0: " + initializationString + " For Player " + str(self.numPlayer))

        # Grid 2 Layout
        else:

            # Button 0 - Horizontal Slider Only

            initializationString = (horizontalSlider + ':' + self.randomNameChar(self.sliderNames)) + '?'
            print(initializationString)

            # Button 1 - Vertical Slider or Switch

            randNum = self.randomNumber(switchVSliderAmount)
            buttonOption = switchVSlider[randNum]
            initializationString += (buttonOption[self.randomNumber(len(buttonOption))]
            + ':' + self.randomNameChar(self.switchVSliderNames[randNum])+ '?')
            print(initializationString)

            # Button 2 - Switch Only

            initializationString += (switchOptions[self.randomNumber(switchAmount)]
                                     + ':' + self.randomNameChar(self.switchNames) + '?')
            print(initializationString)

            # Button 3 - Press Only

            initializationString += (pressOptions + ':' + self.randomNameChar(self.pressNames))
            print(initializationString)

        print("Switch: " + str(self.switchNames))
        print("Slider: " + str(self.sliderNames))
        print("Press: " + str(self.pressNames))



    def connectionMade(self):

        print("Successfully connected with Player " + str(self.numPlayer))
        print("Current Players List: " + str(self.factory.players))
        # Initialization of Grid/Buttons
        self.initializeGrid()
        # Initialize a grid from grid array, use random function

    def connectionLost(self, reason):

        self.factory.connections -= 1
        self.factory.players.remove(self)
        print("The connection for player: " + str(self.numPlayer) + " was lost. "
              + str(self.factory.connections) + " are left")

    def lineReceived(self, line):

        """     if self.factory.connections == 2:
                print("Line Received from Player " + str(self.numPlayer) + '\n' + line)
            for player in self.factory.players:
                if player != self:
                    print("Sending data to Player " + str(player.numPlayer))
                    player.sendLine(line)
        """
class ServerFactory(Factory):

    def __init__(self):

        print("Initiliazing ServerFactory...")
        print("Attemping to create TCP Endpoint for Server with:\n"
        + "Port: " + str(portNumber) + "\nIP Address: " + ipAddress)

        self.players = []
        self.connections = 0

        print("Number of Connections: " + str(self.connections))

    def buildProtocol(self, addr):

        if self.connections <= 2:

            self.connections += 1
            print("Number of Connections: " + str(self.connections))

        else:
            print("2 Players Max! Not allowing anymore connections")

        return Server(self)


try:

    serverFactory = ServerFactory()
    reactor.listenTCP(portNumber, serverFactory, numQueues, ipAddress)

    print("Successfully created Socket...")

except CannotListenError:
    print("Error creating socket")

reactor.run()
