from cgitb import reset
import socket
import pygame
import json


class dsRunner():
    def setup(self):
        # Connect to server
        self.ClientSocket = socket.socket()
        address = '192.168.1.102'
        port = 5000
        connectionSuccessful = False

        print('Waiting for connection')

        try:
            self.ClientSocket.connect((address, port))

        except socket.error as e:
            print(str(e))

        # ! Test if this is needed 
        # self.ClientSocket.send(str.encode("TEST"))
        # Expect test message
        #_response = self.ClientSocket.recv(1024)
        #print(_response.decode('utf-8'))
        # ! ---------------------------------->

        while  not connectionSuccessful:
            # Send test message
            self.ClientSocket.send(str.encode('dsRunner'))
            # Wait for response 
            _response = self.ClientSocket.recv(1024)
            print(_response)
            # Validate 
            if _response.decode('utf-8') == 'dsRunner':
                print('Connected')
                connectionSuccessful = True
                        
    def startInput(self):
        pygame.init()

        #waiting for user to plug in controller
        #connecting to controller and initialize

        xboxcontroller = pygame.joystick.Joystick(0)
        xboxcontroller.init()

        #starting loop to obtain x and y controller analog values
        #creating variables to hold x and y value from controller
        left_analog_y_value = 0.0
        right_analog_x_value = 0.0

        while True:

            pygame.event.get()

            #storing analog input from x and y by converting to type float
            left_analog_y_value = float(format(xboxcontroller.get_axis(1)))
            right_analog_x_value = float(format(xboxcontroller.get_axis(4)))

            #uploading x and y analog values to network table
            _data = {}
            _data['RightStickXValue'] = right_analog_x_value
            _data['LeftStickYValue']  = left_analog_y_value


            data = data = json.dumps(_data)
            self.ClientSocket.send(str.encode(data))

            response = self.ClientSocket.recv(1024) 
            print(response.decode('utf-8'))

            # print(self.ClientSocket.recv(1024).decode('utf-8'))

            print("Left Analog Stick: {}\t Right Analog Stick: {}".format(xboxcontroller.get_axis(1),  # left stick y axis
                                                                xboxcontroller.get_axis(4)))  # right stick x axis
    
    
    def keyboardTest(self):
        """
        The function takes in an input, encodes it, sends it to the server, and then decodes the response
        from the server.
        """

        while True:

            _keyStroke = input()

            #uploading x and y analog values to network table
            _data = {}
            _data['RightStickXValue'] = _keyStroke + '_1'
            _data['LeftStickYValue']  = _keyStroke + '_2'

            data = data = json.dumps(_data)
            self.ClientSocket.send(str.encode(data))

            response = self.ClientSocket.recv(1024) 
            print(response.decode('utf-8'))




if __name__ == '__main__':
    runner = dsRunner()
    runner.setup()

    # Reverse the commenting for these two to change control type
    runner.keyboardTest()
    # runner.startInput()
