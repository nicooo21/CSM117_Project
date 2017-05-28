from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import string, sys
from collections import defaultdict
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

# Available Names
switchNames = ['a', 'b', 'c', 'd', 'e', 'f']
sliderNames = ['a', 'b', 'c', 'd', 'e', 'f']
pressNames = ['a', 'b', 'c', 'd', 'e', 'f']

# Name Combinations
optionNames = [switchNames, sliderNames, pressNames]
switchVSliderNames = [switchNames, sliderNames]
switchPressNames = [switchNames, pressNames]

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
        self.state = 'startGame'

    def randomNumber(self, length):
        return randint(0, length - 1)

    def randomNameChar(self, names):
        nameChar = names[self.randomNumber(len(names))]
        print('char: ' + nameChar)
        names.remove(nameChar)
        print("list is now: " + str(names))
        return nameChar

    def randMultOption(self, amount, list, names):
           
        randNum = self.randomNumber(amount)
        buttonOption = list[randNum]
        buttonChar = buttonOption[self.randomNumber(len(buttonOption))]
        nameChar = self.randomNameChar(names[randNum])
    
        return [buttonChar, nameChar]

    def initializeGrid(self):
        # Randomize Grid (Either one or zero)
        self.gridNumber = self.randomNumber(gridAmount)
        print ("Grid Layout: " + str(self.gridNumber) + " For Player " + str(self.numPlayer))
        # Randomize Buttons Depending on Grid
        # Grid 1 Layout
        if self.gridNumber == 0:
            # Initialize Button 0 - Switch or Press + Name
            buttonChar, nameChar = self.randMultOption(switchPressAmount, switchPress, switchPressNames)

            self.initializationString = (buttonChar + ':' + nameChar + '?')
            print(self.initializationString)
            # Initialize Button 1 - Horizontal Slider + Name

            nameChar = self.randomNameChar(sliderNames)
            self.initializationString += horizontalSlider + ':' + nameChar + '?'
            print(self.initializationString)

            # Initialize Button 2 - Anything + Name
            
            buttonChar, nameChar = self.randMultOption(numOptions, totalOptions, optionNames)
            self.initializationString += ( buttonChar + ':' + nameChar + '?')
            print (self.initializationString)

            # Initialize Button 3 - Switch or Vertical Slider

            buttonChar, nameChar = self.randMultOption(switchVSliderAmount, switchVSlider, switchVSliderNames )
            self.initializationString += (buttonChar + ':' + nameChar)
            print("Final String for Grid 0: " + self.initializationString + " For Player " + str(self.numPlayer))
            

        # Grid 2 Layout
        else:

            # Button 0 - Horizontal Slider Only

            nameChar = self.randomNameChar(sliderNames)
            self.initializationString = (horizontalSlider + ':' + nameChar + '?')
            
            print(self.initializationString)
            # Button 1 - Vertical Slider or Switch
            
            buttonChar, nameChar = self.randMultOption(switchVSliderAmount, switchVSlider, switchVSliderNames )
            self.initializationString += (buttonChar + ':' + nameChar + '?')
            
            print(self.initializationString)
            # Button 2 - Switch Only

            buttonChar = switchOptions[self.randomNumber(switchAmount)]
            nameChar = self.randomNameChar(switchNames)
            self.initializationString += ( buttonChar + ':' + nameChar + '?')
            print(self.initializationString)

            # Button 3 - Press Only
            nameChar = self.randomNameChar(pressNames)
            self.initializationString += (pressOptions + ':' + nameChar)
            print(self.initializationString)

        print("Switch: " + str(switchNames))
        print("Slider: " + str(sliderNames))
        print("Press: " + str(pressNames))
        print(self.initializationString)
        self.sendLine(self.gridNumber + '%' + self.initializationString)


    def connectionMade(self):

        print("Successfully connected with Player " + str(self.numPlayer))
        print("Current Players List: " + str(self.factory.players))
        self.sendLine("You are Player " + str(self.numPlayer))
        # Initialization of Grid/Buttons


    def connectionLost(self, reason):

        if self.factory.connections > 0:
            self.factory.connections -= 1
            self.factory.players.remove(self)
            print("The connection for Player " + str(self.numPlayer) + " was lost. "
                  + str(self.factory.connections) + " connection(s) remain.")

    def shareGrid(self):
        self.initializeGrid()
        for player in self.factory.players:
            if player is not self:
                player.sendLine(self.initializationString)


    def lineReceived(self, line):

        print ("YO")
        """
        if self.state is 'startGame':
            self.readyStart = line
            readyCheck = 0
            for player in self.factory.players:
                if player.readyStart is '1':
                    readyCheck += 1
            if readyCheck == self.factory.connections and self.factory.connections >= 1: # change to > 1 after test
                self.initializeGrid()
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
