from CONSTANTS import *
from client_sockets import *

'''
    We provide the main client class here. It is a free
    framework where you can implenment whatever you want.

    We also provide a simple CLI menu which cantains two menus:
        1. Main menu: If you are not in a meeting, you should use this menu
            1.1 Create a meeting
            1.2 Join a meeting
        2. Meeting menu: If you are in a meeting, you should use this menu
            2.1. (Stop) Share screen
            2.2. (Stop) Control other's screen
            2.3. (Stop) Control my screen
            2.4. (Stop) Share video
            2.5. (Stop) Share audio
            2.6. Leave a meeting
            2.7. Show current meeting members
        It is a simple meeting menu. Taking the first action for example,
        if you have not shared the screen, you start to share.
        Otherwise, you would stop sharing.
    You can use the variable of (client.state) and (client.changed) together to determine the
    CIL menu.

    If you want to implement the GUI directly, you can delete the CLI menu
    related code.
'''

class Client():
    '''
        This is a client class. 
        Feel free to define functions that you need here.
        The client would contain the ClientSocket(or its subclasses)
    '''
    def __init__(self,addr,sport = None):
        '''
            @Parameters
                addr: A dictionary of server address
                    addr = {
                        'xx': (ip,PORT1),
                        'yy': (ip,PORT2),
                        ...
                    }
        '''
        # Create ClientSocket (including its subclasses)
        # self.xx_sockets = XXSocket(addr['xx'],self,sport)
        # self.yy_sockets = YYSocket(addr['yy'],self,sport)
        # ...

        # You can initiate whatever you think is needed

        # Here we define two variables for CIL menu
        self.state = MAIN
        self.changed = True

    # Here we define an action function to change the CIL menu
    # based on different actions
    def action(self,action):
        if self.state == MAIN:
            if action == '1':
                self.create_meeting()
            elif action == '2':
                sid = input("Please input the meeting id:")
                while not str.isdigit(sid):
                    sid = input("Please input the meeting id:")
                sid = int(sid)
                self.join_meeting(sid)
        elif self.state == MEETING:
            '''
                Please complete following codes
            '''
            if action == '1':
                pass
            elif action == '2':
                pass
            #elif ...

    # All the functions defined bellow are not a must
    # You can define whatever function as you like
    def create_meeting(self):
        pass

    def join_meeting(self,sid):
        pass

if __name__ == "__main__":
    # The ip address of the server
    ip = '127.0.0.1'
    # The example ports of the server
    # You can use one or more than one sockets
    address = {
        'xx': (ip,XXPORT),
        'yy': (ip,YYPORT),
    }
    client = Client(address)
    # A CIL menu loop
    while True:
        if client.changed and client.state == MAIN:
            client.changed = False
            # Main menu
            print("1. Create a meeting")
            print("2. Join a meeting")
            action = input("Action:")
            client.action(action)
        elif client.changed and client.state == MEETING:
            client.changed = False
            print("You are in the meeting: %d"%client.sid)
            # meeting menu
            print("1. (Stop) Share screen")
            print("2. (Stop) Control other's screen")
            print("3. (Stop) Control my screen")
            print("4. (Stop) Share video")
            print("5. (Stop) Share audio")
            print("6. Leave a meeting")
            print("7. Show current meeting members")
            action = input("Action:")
            client.action(action)