from CONSTANTS import *
from client_sockets import *
import ctrl
import bectrl

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

    def __init__(self, addr, sport=None):
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
        self.video_sockets = ClientSocket(addr['xx'], self, sport)
        self.audio_sockets = AudioClientSocket(addr['yy'], self, sport)
        self.msg_sockets = msg_ClientSocket(addr['zz'], self, sport)
        self.desktop_sockets = desktop_ClientSocket(addr['aa'], self, sport)
        # You can initiate whatever you think is needed
        # Here we define two variables for CIL menu
        self.state = MAIN
        self.changed = True
        self.video_flag = False
        self.audio_flag = False
        self.share_flag = False
        self.control_flag = False
        self.control_conn = None
        self.mid = None
        self.once = False

    # Here we define an action function to change the CIL menu
    # based on different actions
    def action(self, action):
        if self.state == MAIN:
            if action == '1':
                self.create_meeting()
            elif action == '2':
                sid = input("Please input the meeting id:")
                self.join_meeting(sid)
                self.mid = sid
        elif self.state == MEETING:
            '''
                Please complete following codes
            '''
            if action == '1':
                self.share_screen()
            elif action == '2':
                self.control_others()
            elif action == '3':
                self.control_my()
            elif action == '4':
                self.share_video()
            elif action == '5':
                self.share_audio()
            elif action == '6':
                self.leaving_meeting()
            elif action == '7':
                self.show_members()
            elif action == '8':
                self.closing_meeting()

    # All the functions defined bellow are not a must
    # You can define whatever function as you like
    def create_meeting(self):
        self.msg_sockets.send_msg('1')
        meeting_id = self.msg_sockets.receive_data()
        return meeting_id

    def control_others(self):
        control = input("Please input the control ip:")
        self.msg_sockets.send_msg('ip' + str(control))
        agree = self.msg_sockets.receive_data()
        if agree == 'No':
            print('No')
        elif agree == 'Yes':
            print('Yes')
            ctrl.work()
            print('Stop Control')
        else:
            print('Control Wrong')

    def control_my(self):
        if not self.control_flag:
            accept = self.msg_sockets.receive_data()
            self.msg_sockets.send_msg(accept)
            if accept == 'y':
                print("yes!")
                self.control_conn = bectrl.beControl()
                self.control_flag = True
        else:
            bectrl.stopControl(self.control_conn)
            self.control_flag = False

    def join_meeting(self, sid):
        self.msg_sockets.send_msg(sid)
        ok = self.msg_sockets.receive_data()
        if ok and not self.once:
            self.state = MEETING
            self.video_sockets.receive_thread.start()
            self.video_sockets.send_thread.start()
            self.audio_sockets.receive_thread.start()
            self.audio_sockets.send_thread.start()
            self.desktop_sockets.send_thread.start()
            self.desktop_sockets.receive_thread.start()
            self.once = True
        elif ok:
            self.state = MEETING
        return ok


    def share_screen(self):
        if not self.share_flag and not self.desktop_sockets.receive:
            self.desktop_sockets.agree = True
            self.share_flag = True
        else:
            self.desktop_sockets.agree = False
            self.share_flag = False

    def share_video(self):
        if not self.video_flag:
            self.video_sockets.open_cap()
            self.video_flag = True
        else:
            self.video_sockets.close_cap()
            self.video_flag = False

    def share_audio(self):
        if not self.audio_flag:
            self.audio_sockets.open_stream()
            self.audio_flag = True
        else:
            self.audio_sockets.close_stream()
            self.audio_flag = False

    def leaving_meeting(self):
        self.msg_sockets.send_msg('2')
        # self.video_sockets.__del__()
        # self.audio_sockets.__del__()
        self.msg_sockets.receive_data()
        self.mid = None
        self.state = MAIN

    def show_members(self):
        self.msg_sockets.send_msg('3')
        member_list = self.msg_sockets.receive_data()
        return member_list

    def closing_meeting(self):
        self.msg_sockets.send_msg('close'+str(self.mid))
        success = self.msg_sockets.receive_data()
        if success == 'Close Success':
            self.mid = None
            self.state = MAIN

if __name__ == "__main__":
    # The ip address of the serverip
    # ip = '10.24.184.6'
    # ip = '10.15.135.9'
    # ip = '10.24.240.125'
    # ip = '10.24.253.245'
    # ip = '192.168.46.24' #24/61
    # ip = '192.168.13.61'
    # ip = '127.0.0.1'
    # ip = '192.168.96.24'
    ip = '10.24.81.213'

    # The example ports of the server
    # You can use one or more than one sockets
    address = {
        'xx': (ip, XXPORT),
        'yy': (ip, YYPORT),
        'zz': (ip, ZZPORT),
        'aa': (ip, AAPORT)
    }
    client = Client(address)
    # A CIL menu loop
    # print("test")
    while True:
        # print("loop")
        if client.changed and client.state == MAIN:
            # client.changed = False
            # Main menu
            print("1. Create a meeting")
            print("2. Join a meeting")
            action = input("Action:")
            client.action(action)
        elif client.changed and client.state == MEETING:
            # client.changed = False
            print("You are in the meeting: %s" % client.mid)
            # meeting menu
            print("1. (Stop) Share screen")
            print("2. (Stop) Control other's screen")
            print("3. (Stop) Control my screen")
            print("4. (Stop) Share video")
            print("5. (Stop) Share audio")
            print("6. Leave a meeting")
            print("7. Show current meeting members")
            print("8. Close a meeting")
            action = input("Action:")
            client.action(action)
